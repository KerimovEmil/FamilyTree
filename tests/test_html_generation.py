from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))

from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement
from utils import (
    generate_id_from_pointer,
    extract_name_parts,
    get_individual_relative_path,
)
from data_extraction import get_name, get_birth_data, get_death_data
from html_generation import (
    escape_text,
    generate_html_for_individual,
    generate_index_html,
    generate_individuals_html,
    generate_surname_pages,
    generate_relationship_finder_html,
    build_family_graph,
    generate_interactive_graph_html,
    linkify_individual_references,
)


def build_test_environment(tmp_path):
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'sample.ged')
    parser = Parser()
    parser.parse_file(fixture_path)

    individuals_data = {}
    for element in parser.get_root_child_elements():
        if isinstance(element, IndividualElement):
            ind_id = generate_id_from_pointer(element.get_pointer())
            name = get_name(element)
            surname, given_name = extract_name_parts(name)
            birth_date = get_birth_data(element)
            death_date = get_death_data(element)
            rel_path = get_individual_relative_path(surname, given_name, ind_id)

            individuals_data[ind_id] = {
                'name': name,
                'birth_date': birth_date,
                'death_date': death_date,
                'surname': surname,
                'given_name': given_name,
                'path': rel_path,
                'element': element
            }

    return parser, individuals_data


def test_escape_text():
    assert escape_text(None) == ""
    assert escape_text("Hello & World") == "Hello &amp; World"
    assert escape_text("<script>alert('xss')</script>") == "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"
    assert escape_text('"quoted"') == "&quot;quoted&quot;"


def test_generate_html_for_individual_with_events_and_attributes(tmp_path):
    parser, individuals_data = build_test_environment(tmp_path)
    # Find John Doe
    john_id = None
    for ind_id, data in individuals_data.items():
        if data['name'] == "Doe, John":
            john_id = ind_id
            break

    assert john_id is not None
    john_element = individuals_data[john_id]['element']
    html = generate_html_for_individual(parser, john_element, individuals_data)

    # Individual details
    assert "Doe, John" in html
    assert "New York, USA" in html
    assert "Boston, USA" in html
    assert "Engineer" in html
    assert "12345" in html  # RFN attribute
    assert "Alternative Names" in html
    assert "Johnny Doe" in html
    assert "(Nickname)" in html
    assert "Birth" in html
    assert "Death" in html

    # Milestone Age & Interactive Graph deep-link assertions
    assert "Age at Death" in html
    assert "50 years old" in html
    assert "Age: 50" in html
    assert 'interactive_graph.html?indi=I1' in html
    assert 'relationship.html?p1=I1' in html

    # Notes & Photos rendering assertions
    assert 'id="notes"' in html
    assert "Distinguished engineer and family historian." in html
    assert "Second line of biographical note." in html
    assert 'images/people/Hadjiismail_Gulcheev.jpg' in html

    # Chronological events order in #events section (Birth -> Occupation -> Death)
    events_section = html[html.find('id="events"'):html.find('</div>', html.find('id="events"'))]
    birth_idx = events_section.find("Birth")
    occu_idx = events_section.find("Occupation")
    death_idx = events_section.find("Death")
    assert -1 < birth_idx < occu_idx < death_idx

    # Family & Single Parent assertions
    assert "Smith, Jane" in html
    assert "Doe, Junior" in html
    assert "Doe, Solo" in html
    assert "Family of Doe, John and Unknown" in html

    # Valid links
    assert 'href="../../ppl/smith/jane_' in html
    assert 'href="../../ppl/doe/junior_' in html
    assert 'href="../../ppl/doe/solo_' in html


def test_generate_html_for_single_parent_child(tmp_path):
    parser, individuals_data = build_test_environment(tmp_path)
    # Solo Doe has John as father, no mother
    solo_id = None
    for ind_id, data in individuals_data.items():
        if data['name'] == "Doe, Solo":
            solo_id = ind_id
            break

    assert solo_id is not None
    solo_element = individuals_data[solo_id]['element']
    html = generate_html_for_individual(parser, solo_element, individuals_data)

    assert "Doe, Solo" in html
    assert "Doe, John" in html
    # Father row exists
    assert 'href="../../ppl/doe/john_' in html


def test_site_generation_end_to_end(tmp_path, monkeypatch):
    parser, individuals_data = build_test_environment(tmp_path)

    # Monkeypatch constants directory targets to run in tmp_path
    ppl_dir = tmp_path / "ppl"
    surnames_dir = tmp_path / "surnames"
    ppl_dir.mkdir()
    surnames_dir.mkdir()

    monkeypatch.chdir(tmp_path)

    # Generate all individual files
    for ind_id, data in individuals_data.items():
        content = generate_html_for_individual(parser, data['element'], individuals_data)
        file_path = tmp_path / data['path']
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')

    # Generate index, individuals, surname pages, and relationship finder
    generate_index_html(individuals_data)
    generate_individuals_html(individuals_data)
    generate_surname_pages(individuals_data)
    generate_relationship_finder_html(parser, individuals_data)

    # Verify generated files exist
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "individuals.html").exists()
    assert (tmp_path / "surnames" / "doe.html").exists()
    assert (tmp_path / "surnames" / "smith.html").exists()

    # Verify index.html content
    index_content = (tmp_path / "index.html").read_text(encoding='utf-8')
    assert "surnames/doe.html" in index_content
    assert "surnames/smith.html" in index_content
    assert 'id="searchInput"' in index_content
    assert 'id="clearSearch"' in index_content
    assert 'id="searchCount"' in index_content
    assert 'filterTable()' in index_content
    assert 'clearSearchFilter()' in index_content

    # Verify individuals.html content
    ind_content = (tmp_path / "individuals.html").read_text(encoding='utf-8')
    assert "Doe, John" in ind_content
    assert "Smith, Jane" in ind_content
    assert "Doe, Junior" in ind_content
    assert "Doe, Solo" in ind_content
    assert 'id="searchInput"' in ind_content
    assert 'id="clearSearch"' in ind_content
    assert 'id="searchCount"' in ind_content
    assert 'filterTable()' in ind_content
    assert 'clearSearchFilter()' in ind_content

    # Verify surnames page content
    doe_content = (tmp_path / "surnames" / "doe.html").read_text(encoding='utf-8')
    assert 'id="searchInput"' in doe_content
    assert 'id="clearSearch"' in doe_content
    assert 'id="searchCount"' in doe_content
    assert 'filterTable()' in doe_content
    assert 'clearSearchFilter()' in doe_content
    assert 'id="dataTable"' in doe_content

    # Verify relationship.html content
    assert (tmp_path / "relationship.html").exists()
    rel_content = (tmp_path / "relationship.html").read_text(encoding='utf-8')
    assert 'id="p1Input"' in rel_content
    assert 'id="p2Input"' in rel_content
    assert 'id="swapBtn"' in rel_content
    assert 'id="findBtn"' in rel_content
    assert 'id="familyGraphData"' in rel_content
    assert 'Doe, John' in rel_content


def test_interactive_graph_page():
    root = Path(__file__).resolve().parent.parent
    graph_file = root / "interactive_graph.html"
    assert graph_file.exists()
    content = graph_file.read_text(encoding="utf-8")
    assert 'id="graph-svg"' in content
    assert 'id="viewSelect"' in content
    assert 'id="personSearch"' in content
    assert 'id="homeBtn"' in content
    assert 'id="clearSearchBtn"' in content
    assert 'id="fitViewBtn"' in content
    assert 'id="familyGraphData"' in content
    assert 'id="gedcomData"' in content
    assert "js/topola-bundle.min.js" in content
    assert "js/interactive_graph.js" in content


def test_generate_interactive_graph_html(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    parser, individuals_data = build_test_environment(tmp_path)

    ged_dir = tmp_path / "ged"
    ged_dir.mkdir()
    (ged_dir / "family_tree.ged").write_text("0 HEAD\n1 SOUR TEST\n0 TRLR", encoding="utf-8")

    generate_interactive_graph_html(parser, individuals_data)

    graph_file = tmp_path / "interactive_graph.html"
    assert graph_file.exists()
    content = graph_file.read_text(encoding="utf-8")
    assert 'id="graph-svg"' in content
    assert 'id="familyGraphData"' in content
    assert '0 HEAD' in content


def test_build_family_graph(tmp_path):
    parser, individuals_data = build_test_environment(tmp_path)
    graph = build_family_graph(parser, individuals_data)

    # I1 is John Doe
    assert "I1" in graph
    john = graph["I1"]
    assert john["name"] == "Doe, John"
    assert john["gender"] == "male"
    assert "I2" in john["spouses"] # Jane Smith
    assert "I3" in john["children"] # Junior Doe
    assert "I4" in john["children"] # Solo Doe

    # I3 is Junior Doe
    assert "I3" in graph
    junior = graph["I3"]
    assert "I1" in junior["parents"]
    assert "I2" in junior["parents"]

    # I4 is Solo Doe (single parent of John)
    assert "I4" in graph
    solo = graph["I4"]
    assert "I1" in solo["parents"]
    assert len(solo["parents"]) == 1


def test_linkify_individual_references():
    individuals_data = {
        'id_john': {'path': 'ppl/doe/john_123.html'},
        'id_jane': {'path': 'ppl/smith/jane_456.html'}
    }
    # Mock generate_id_from_pointer behavior for the test
    # In real code: generate_id_from_pointer("@I1@") -> md5 prefix
    # Let's import generate_id_from_pointer
    from utils import generate_id_from_pointer

    id1 = generate_id_from_pointer("@I1@")
    id2 = generate_id_from_pointer("@I2@")
    ind_data = {
        id1: {'path': 'ppl/doe/john_123.html'},
        id2: {'path': 'ppl/smith/jane_456.html'}
    }

    note_text = "Paternal grandfather of John Doe (@I1@) and Jane Smith (@I2@)."
    result = linkify_individual_references(note_text, ind_data)
    assert '<a href="../../ppl/doe/john_123.html">John Doe</a>' in result
    assert '<a href="../../ppl/smith/jane_456.html">Jane Smith</a>' in result
    assert '@I1@' not in result
    assert '@I2@' not in result
    assert 'Paternal grandfather of ' in result
