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
    assert "Birth" in html
    assert "Death" in html

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

    # Generate index, individuals, and surname pages
    generate_index_html(individuals_data)
    generate_individuals_html(individuals_data)
    generate_surname_pages(individuals_data)

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
    assert 'filterTable()' in index_content

    # Verify individuals.html content
    ind_content = (tmp_path / "individuals.html").read_text(encoding='utf-8')
    assert "Doe, John" in ind_content
    assert "Smith, Jane" in ind_content
    assert "Doe, Junior" in ind_content
    assert "Doe, Solo" in ind_content
    assert 'id="searchInput"' in ind_content
    assert 'filterTable()' in ind_content
