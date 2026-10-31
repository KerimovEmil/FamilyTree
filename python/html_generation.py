#!/usr/bin/env python3
"""
Functions for generating HTML content from GEDCOM data with new directory structure.
"""

import html
import re
import os
from utils import (
    generate_id_from_pointer, get_surname_file_path, get_surname_relative_path,
    extract_name_parts
)
from data_extraction import (
    get_name, get_gender, get_birth_data, get_birth_place, get_death_data,
    get_death_place, has_death_event, get_occupation, get_attributes,
    get_notes, get_photos, get_parents, get_families, parse_date, calculate_age, get_alternative_names
)

def escape_text(val):
    """Safely escape text for interpolation into HTML templates."""
    if val is None:
        return ""
    return html.escape(str(val))

import json
from gedcom.element.individual import IndividualElement
from constants import (
    HTML_TEMPLATE, EVENT_ROW_TEMPLATE, ATTRIBUTES_SECTION_TEMPLATE,
    ATTRIBUTE_ROW_TEMPLATE, NOTES_SECTION_TEMPLATE, PHOTO_SECTION_TEMPLATE,
    PARENTS_TEMPLATE, PARENT_ROW_TEMPLATE, SIBLING_ROW_TEMPLATE, FAMILIES_TEMPLATE,
    FAMILY_ROW_TEMPLATE, CHILD_ROW_TEMPLATE, PEDIGREE_TEMPLATE,
    ANCESTORS_TEMPLATE, INDEX_HTML_TEMPLATE, INDIVIDUALS_HTML_TEMPLATE,
    SURNAME_ENTRY_TEMPLATE, INDIVIDUAL_ENTRY_TEMPLATE, SURNAME_PAGE_TEMPLATE,
    SURNAME_INDIVIDUAL_ENTRY_TEMPLATE, RELATIONSHIP_FINDER_TEMPLATE, INTERACTIVE_GRAPH_TEMPLATE, GEDCOM_FILE, SURNAMES_DIR
)

def get_path_for_individual(individual_id, individuals_data):
    """Get the relative path for an individual from individuals_data."""
    if individual_id in individuals_data and 'path' in individuals_data[individual_id]:
        return individuals_data[individual_id]['path']
    print(f"Warning: Could not find path for individual {individual_id}")
    return ""

def generate_parents_section(gedcom_parser, individual, individual_id, individuals_data):
    """Generate the HTML for the parents section."""
    parents_info = get_parents(gedcom_parser, individual)
    if not parents_info:
        return ""

    parents_rows = []

    # Add father row
    if parents_info['father']:
        father = parents_info['father']
        father_id = generate_id_from_pointer(father.get_pointer())
        father_path = get_path_for_individual(father_id, individuals_data)
        father_name = escape_text(get_name(father))
        father_birth = escape_text(get_birth_data(father))
        father_death = escape_text(get_death_data(father))

        parents_rows.append(PARENT_ROW_TEMPLATE.format(
            relation="Father",
            parent_path=father_path,
            parent_name=father_name,
            parent_birth=father_birth,
            parent_death=father_death
        ))

    # Add mother row
    if parents_info['mother']:
        mother = parents_info['mother']
        mother_id = generate_id_from_pointer(mother.get_pointer())
        mother_path = get_path_for_individual(mother_id, individuals_data)
        mother_name = escape_text(get_name(mother))
        mother_birth = escape_text(get_birth_data(mother))
        mother_death = escape_text(get_death_data(mother))

        parents_rows.append(PARENT_ROW_TEMPLATE.format(
            relation="Mother",
            parent_path=mother_path,
            parent_name=mother_name,
            parent_birth=mother_birth,
            parent_death=mother_death
        ))

    # Add self row
    individual_name = escape_text(get_name(individual))
    individual_birth = escape_text(get_birth_data(individual))
    individual_death = escape_text(get_death_data(individual))

    parents_rows.append(f"""
<tr>
    <td class="ColumnAttribute">&nbsp;&nbsp;&nbsp;&nbsp;</td>
    <td class="ColumnValue">&nbsp;&nbsp;&nbsp;&nbsp;<b>{individual_name}</b></td>
    <td class="ColumnDate">{individual_birth}</td>
    <td class="ColumnDate">{individual_death}</td>
    <td class="ColumnValue"></td>
</tr>
""")

    # Add siblings rows
    for sibling in parents_info['siblings']:
        sibling_id = generate_id_from_pointer(sibling.get_pointer())
        sibling_path = get_path_for_individual(sibling_id, individuals_data)
        sibling_name = escape_text(get_name(sibling))
        sibling_birth = escape_text(get_birth_data(sibling))
        sibling_death = escape_text(get_death_data(sibling))
        sibling_gender = get_gender(sibling)

        relation = "Sister" if sibling_gender == "female" else "Brother"

        sibling_link = f'<a href="../../{sibling_path}">{sibling_name}</a>'

        parents_rows.append(SIBLING_ROW_TEMPLATE.format(
            relation=relation,
            sibling_link=sibling_link,
            sibling_birth=sibling_birth,
            sibling_death=sibling_death
        ))

    return PARENTS_TEMPLATE.format(parents_rows=''.join(parents_rows))

def generate_families_section(gedcom_parser, individual, individual_id, individuals_data):
    """Generate the HTML for the families section."""
    families_info = get_families(gedcom_parser, individual)
    if not families_info:
        return ""

    families_rows = []
    individual_gender = get_gender(individual)

    for family in families_info:
        husband = family['husband']
        wife = family['wife']
        children = family['children']

        # Determine spouse based on individual's gender
        if individual_gender == "male":
            spouse = wife
            spouse_relation = "Wife"
        else:
            spouse = husband
            spouse_relation = "Husband"

        # Skip only families with neither a spouse nor any children
        if not spouse and not children:
            continue

        if spouse:
            spouse_id = generate_id_from_pointer(spouse.get_pointer())
            spouse_path = get_path_for_individual(spouse_id, individuals_data)
            spouse_name_esc = escape_text(get_name(spouse))
            spouse_birth_esc = escape_text(get_birth_data(spouse))
            spouse_death_val = get_death_data(spouse)
            spouse_death_esc = escape_text(spouse_death_val) if spouse_death_val else "..."
            spouse_html = (
                f'<a href="../../{spouse_path}">{spouse_name_esc}</a>\n'
                f'     ( *\n    {spouse_birth_esc}\n     +\n'
                f'    {spouse_death_esc}\n     )'
            )
        else:
            spouse_html = 'Unknown'

        # Generate children rows
        children_rows = []
        for child in children:
            child_id = generate_id_from_pointer(child.get_pointer())
            child_path = get_path_for_individual(child_id, individuals_data)
            child_name = escape_text(get_name(child))
            child_birth = escape_text(get_birth_data(child))
            child_death = escape_text(get_death_data(child))

            children_rows.append(CHILD_ROW_TEMPLATE.format(
                child_path=child_path,
                child_name=child_name,
                child_birth=child_birth,
                child_death=child_death
            ))

        # Get husband and wife names for the family title
        husband_name = escape_text(get_name(husband) if husband else "Unknown")
        wife_name = escape_text(get_name(wife) if wife else "Unknown")

        families_rows.append(FAMILY_ROW_TEMPLATE.format(
            husband_name=husband_name,
            wife_name=wife_name,
            spouse_relation=spouse_relation,
            spouse_html=spouse_html,
            children_rows=''.join(children_rows)
        ))

    return FAMILIES_TEMPLATE.format(families_rows=''.join(families_rows))

def generate_events_rows(element):
    """Generate rows for the Events table sorted chronologically with milestone ages."""
    birth_date = get_birth_data(element)
    events = []

    # Birth event
    birth_place = get_birth_place(element)
    events.append({
        'name': 'Birth',
        'date': birth_date,
        'place': birth_place,
        'description': '',
        'type_order': 0,
        'parsed_date': parse_date(birth_date),
    })

    # Death event
    if has_death_event(element):
        death_date = get_death_data(element)
        death_place = get_death_place(element)
        death_age = calculate_age(birth_date, death_date)
        desc = f"Age: {death_age}" if death_age else ""
        events.append({
            'name': 'Death',
            'date': death_date,
            'place': death_place,
            'description': desc,
            'type_order': 2,
            'parsed_date': parse_date(death_date),
        })

    # Occupation event
    occupation = get_occupation(element)
    if occupation and occupation.strip() and occupation != "&nbsp;":
        events.append({
            'name': 'Occupation',
            'date': '',
            'place': '',
            'description': occupation.strip(),
            'type_order': 1,
            'parsed_date': None,
        })

    birth_parsed = parse_date(birth_date)
    death_parsed = parse_date(get_death_data(element)) if has_death_event(element) else None

    def event_sort_key(ev):
        pd = ev['parsed_date']
        if ev['name'] == 'Birth':
            if pd:
                return (pd[0], pd[1], pd[2], 0)
            return (-9999, 0, 0, 0)
        elif ev['name'] == 'Death':
            if pd:
                return (pd[0], pd[1], pd[2], 2)
            return (9999, 0, 0, 2)
        else:
            if pd:
                return (pd[0], pd[1], pd[2], 1)
            if death_parsed:
                return (death_parsed[0], 0, 0, 1)
            if birth_parsed:
                return (birth_parsed[0], 99, 99, 1)
            return (0, 0, 0, 1)

    sorted_events = sorted(events, key=event_sort_key)

    events_rows = []
    for ev in sorted_events:
        events_rows.append(EVENT_ROW_TEMPLATE.format(
            event_name=escape_text(ev['name']),
            event_date=escape_text(ev['date']),
            event_place=escape_text(ev['place']),
            event_description=escape_text(ev['description'])
        ))

    return '\n'.join(events_rows)

def generate_attributes_section(element):
    """Generate the HTML attributes section if attributes are present."""
    attributes = get_attributes(element)
    if not attributes:
        return ""

    attributes_rows = []
    for attr in attributes:
        attributes_rows.append(ATTRIBUTE_ROW_TEMPLATE.format(
            attr_type=escape_text(attr.get('type', '')),
            attr_value=escape_text(attr.get('value', '')),
            attr_notes=escape_text(attr.get('notes', '')),
            attr_sources=attr.get('sources', '&nbsp;')
        ))

    return ATTRIBUTES_SECTION_TEMPLATE.format(attributes_rows='\n'.join(attributes_rows))

def linkify_individual_references(text, individuals_data):
    """
    Detect references to individuals like 'Name (@I...NUMBER...@)' in notes text,
    and convert the name into a hyperlink pointing to the individual's profile page,
    omitting the raw ID number from the visible text.
    """
    if not individuals_data or '@I' not in text:
        return escape_text(text)

    pattern = re.compile(
        r"(?P<name>(?:[A-Z][a-zA-Z\u00C0-\u024F\u0400-\u04FF']*(?:'s)?(?:\s+(?:[A-Z][a-zA-Z\u00C0-\u024F\u0400-\u04FF']+|uncle|sister))*|her sister))"
        r'\s*\((?P<paren>[^()]*?@(I[0-9a-zA-Z_]+)@[^()]*?)\)'
    )

    last_end = 0
    pieces = []
    for m in pattern.finditer(text):
        pieces.append(escape_text(text[last_end:m.start()]))

        name = m.group('name')
        paren_content = m.group('paren')
        indi_ptr = m.group(3)

        ind_id = generate_id_from_pointer(f"@{indi_ptr}@")
        if ind_id in individuals_data:
            path = individuals_data[ind_id]['path']
            clean_paren = re.sub(rf',?\s*@{indi_ptr}@\s*,?', '', paren_content).strip()
            clean_paren = re.sub(r'^,\s*|,\s*$', '', clean_paren).strip()

            link = f'<a href="../../{path}">{escape_text(name)}</a>'
            if clean_paren:
                pieces.append(f"{link} ({escape_text(clean_paren)})")
            else:
                pieces.append(link)
        else:
            pieces.append(escape_text(m.group(0)))

        last_end = m.end()

    pieces.append(escape_text(text[last_end:]))
    return "".join(pieces)

def generate_notes_section(gedcom_parser, element, individuals_data=None):
    """Generate the HTML notes/biography section if notes are present."""
    notes = get_notes(gedcom_parser, element)
    if not notes:
        return ""

    paragraphs = []
    for note in notes:
        lines = []
        for line in note.splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            if individuals_data:
                lines.append(linkify_individual_references(line_str, individuals_data))
            else:
                lines.append(escape_text(line_str))
        if lines:
            paragraphs.append("<p style=\"margin: 0 0 8px 0;\">" + "<br />".join(lines) + "</p>")

    if not paragraphs:
        return ""

    return NOTES_SECTION_TEMPLATE.format(notes_items='\n'.join(paragraphs))


def generate_photo_section(element):
    """Generate the HTML photo section if OBJE -> FILE photos are present."""
    photos = get_photos(element)
    if not photos:
        return ""

    name_esc = escape_text(get_name(element))
    items = []
    for photo_path in photos:
        norm_path = photo_path.replace('\\', '/').lstrip('/')
        esc_path = escape_text(norm_path)
        items.append(
            f'<a href="../../{esc_path}" target="_blank" title="View full portrait of {name_esc}">'
            f'<img src="../../{esc_path}" alt="Portrait of {name_esc}" '
            f'style="max-width: 180px; border-radius: 6px; border: 1px solid #cbd5e0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />'
            f'</a>'
        )

    return PHOTO_SECTION_TEMPLATE.format(photo_items='\n'.join(items))

def generate_alternative_names_section(element):
    """Generate HTML row for alternative names / spellings in the summary table."""
    alt_names = get_alternative_names(element)
    if not alt_names:
        return ""

    alt_items = []
    for a in alt_names:
        name_esc = escape_text(a['name'])
        label_esc = escape_text(a['label'])
        alt_items.append(f"<span>{name_esc} <small style='color: #666;'>({label_esc})</small></span>")

    alt_html = "<br />\r\n                        ".join(alt_items)
    return f"""<tr>
                        <td class="ColumnAttribute">Alternative Names</td>
                        <td class="ColumnValue">
                        {alt_html}
                        </td>
                    </tr>"""

def generate_html_for_individual(gedcom_parser, element, individuals_data):
    """Generate HTML content for an individual"""
    ptr = element.get_pointer() if element else ""
    individual_id = generate_id_from_pointer(ptr) if ptr else ""
    clean_pointer = ptr.replace('@', '') if ptr else ""
    name = escape_text(get_name(element))
    gender = escape_text(get_gender(element))

    # Age section in summary
    birth_date = get_birth_data(element)
    death_date = get_death_data(element)
    age_section = ""
    if has_death_event(element):
        death_age = calculate_age(birth_date, death_date)
        if death_age:
            age_section = f"""<tr>
                        <td class="ColumnAttribute">Age at Death</td>
                        <td class="ColumnValue">{escape_text(death_age)} years old</td>
                    </tr>"""

    # Generate photo & notes sections
    photo_section = generate_photo_section(element)
    notes_section = generate_notes_section(gedcom_parser, element, individuals_data)
    alt_names_section = generate_alternative_names_section(element)

    # Generate events rows
    events_rows = generate_events_rows(element)

    # Generate attributes section
    attributes_section = generate_attributes_section(element)

    # Generate parents section
    parents_section = generate_parents_section(gedcom_parser, element, individual_id, individuals_data)

    # Generate families section
    families_section = generate_families_section(gedcom_parser, element, individual_id, individuals_data)

    # Generate pedigree section
    pedigree_section = generate_pedigree_section(gedcom_parser, element, individual_id, individuals_data)

    # Generate ancestors section
    ancestors_section = generate_ancestors_section(gedcom_parser, element, individual_id, individuals_data)

    # Fill in the HTML template
    html_content = HTML_TEMPLATE.format(
        name=name,
        gender=gender,
        clean_pointer=clean_pointer,
        age_section=age_section,
        photo_section=photo_section,
        notes_section=notes_section,
        alt_names_section=alt_names_section,
        events_rows=events_rows,
        married_name_section="",
        attributes_section=attributes_section,
        parents_section=parents_section,
        families_section=families_section,
        pedigree_section=pedigree_section,
        ancestors_section=ancestors_section,
    )

    return html_content

def generate_index_html(individuals_data):
    """Generate the index.html file with surname index."""
    # Group individuals by surname
    surnames = {}
    for individual_id, data in individuals_data.items():
        surname = data.get('surname', 'Unknown')
        if surname and surname != '___':
            if surname not in surnames:
                surnames[surname] = []
            surnames[surname].append((individual_id, data))

    # Sort surnames
    sorted_surnames = sorted(surnames.keys())

    # Generate surname entries
    surname_entries = ""
    for surname in sorted_surnames:
        # Sort individuals by given name
        individuals = sorted(surnames[surname], key=lambda x: x[1]['name'])

        # Generate given names HTML
        given_names_html = ""
        for individual_id, data in individuals:
            given_name = escape_text(data.get('given_name', ''))
            path = data.get('path', '')
            name = escape_text(data.get('name', ''))
            given_names_html += f'<a href="{path}" title="{name}">{given_name}</a>, '

        # Remove trailing comma and space
        given_names_html = given_names_html.rstrip(', ')

        # Get the surname page path
        surname_path = get_surname_relative_path(surname)

        # Add surname entry
        surname_entries += SURNAME_ENTRY_TEMPLATE.format(
            surname=escape_text(surname),
            surname_path=surname_path,
            given_names=given_names_html
        )

    # Fill in the template
    html_content = INDEX_HTML_TEMPLATE.format(
        surname_entries=surname_entries
    )

    # Write to file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Generated index.html with new paths")

def generate_individuals_html(individuals_data):
    """Generate the individuals.html file with all individuals."""
    # Sort individuals by name
    sorted_individuals = sorted(individuals_data.items(), key=lambda x: x[1]['name'])

    # Generate individual entries
    individual_entries = ""
    for individual_id, data in sorted_individuals:
        name = escape_text(data.get('name', ''))
        birth_date = escape_text(data.get('birth_date', ''))
        death_date = escape_text(data.get('death_date', ''))
        path = data.get('path', '')

        individual_entries += INDIVIDUAL_ENTRY_TEMPLATE.format(
            path=path,
            name=name,
            birth_date=birth_date,
            death_date=death_date
        )

    # Fill in the template
    html_content = INDIVIDUALS_HTML_TEMPLATE.format(
        individual_entries=individual_entries
    )

    # Write to file
    with open('individuals.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Generated individuals.html with new paths")

def generate_surname_pages(individuals_data):
    """Generate HTML files for each surname."""
    # Create the surnames directory if it doesn't exist
    os.makedirs(SURNAMES_DIR, exist_ok=True)

    # Group individuals by surname
    surnames = {}
    for individual_id, data in individuals_data.items():
        surname = data.get('surname', '___')
        if surname not in surnames:
            surnames[surname] = []
        surnames[surname].append(data)

    # Generate a page for each surname
    for surname, individuals in surnames.items():
        # Sort individuals by given name
        sorted_individuals = sorted(individuals, key=lambda x: x.get('given_name', ''))

        # Generate individual entries
        individual_entries = ""
        for data in sorted_individuals:
            given_name = escape_text(data.get('given_name', ''))
            birth_date = escape_text(data.get('birth_date', ''))
            path = data.get('path', '')

            individual_entries += SURNAME_INDIVIDUAL_ENTRY_TEMPLATE.format(
                path=path,
                given_name=given_name,
                birth_date=birth_date
            )

        # Fill in the template
        html_content = SURNAME_PAGE_TEMPLATE.format(
            surname=escape_text(surname),
            individual_entries=individual_entries
        )

        # Create a safe filename (shared sanitization with index links)
        file_path = get_surname_file_path(surname)

        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Generated surname page for {surname} at {file_path}")


def build_family_graph(gedcom_parser, individuals_data):
    """Build a serializable graph structure from the GEDCOM parser and individuals_data."""
    graph = {}
    for element in gedcom_parser.get_root_child_elements():
        if isinstance(element, IndividualElement):
            ptr = element.get_pointer().replace('@', '')
            ind_id = generate_id_from_pointer(element.get_pointer())
            name = get_name(element)
            gender = get_gender(element)
            birth = get_birth_data(element)
            death = get_death_data(element)
            path = get_path_for_individual(ind_id, individuals_data)

            # Get parents
            parents_info = get_parents(gedcom_parser, element)
            parents = []
            if parents_info:
                if parents_info['father']:
                    parents.append(parents_info['father'].get_pointer().replace('@', ''))
                if parents_info['mother']:
                    parents.append(parents_info['mother'].get_pointer().replace('@', ''))

            # Get families (spouses and children)
            fams = get_families(gedcom_parser, element)
            spouses = []
            children = []
            for fam in fams:
                if fam['husband'] and fam['husband'].get_pointer().replace('@', '') != ptr:
                    sp_id = fam['husband'].get_pointer().replace('@', '')
                    if sp_id not in spouses:
                        spouses.append(sp_id)
                if fam['wife'] and fam['wife'].get_pointer().replace('@', '') != ptr:
                    sp_id = fam['wife'].get_pointer().replace('@', '')
                    if sp_id not in spouses:
                        spouses.append(sp_id)
                for child in fam['children']:
                    c_id = child.get_pointer().replace('@', '')
                    if c_id not in children:
                        children.append(c_id)

            graph[ptr] = {
                'id': ptr,
                'name': name,
                'gender': gender,
                'birth': birth,
                'death': death,
                'path': path,
                'parents': parents,
                'spouses': spouses,
                'children': children
            }

    # Bidirectional reciprocity check
    for pid, data in graph.items():
        for p_parent in data['parents']:
            if p_parent in graph and pid not in graph[p_parent]['children']:
                graph[p_parent]['children'].append(pid)
        for p_child in data['children']:
            if p_child in graph and pid not in graph[p_child]['parents']:
                graph[p_child]['parents'].append(pid)
        for p_spouse in data['spouses']:
            if p_spouse in graph and pid not in graph[p_spouse]['spouses']:
                graph[p_spouse]['spouses'].append(pid)

    return graph


def generate_relationship_finder_html(gedcom_parser, individuals_data):
    """Generate the relationship.html file with embedded graph data and search options."""
    graph = build_family_graph(gedcom_parser, individuals_data)

    # Sort individuals by display name for datalist
    sorted_people = sorted(graph.values(), key=lambda p: p['name'])
    datalist_options = []
    for p in sorted_people:
        dates = ""
        if p['birth'] or p['death']:
            b = f"*{p['birth']}" if p['birth'] else ""
            d = f"+{p['death']}" if p['death'] else ""
            dates = f" ({' '.join(filter(None, [b, d]))})"
        val = f"{p['name']}{dates} [{p['id']}]"
        datalist_options.append(f'                <option value="{escape_text(val)}"></option>')

    people_datalist_options = "\n".join(datalist_options)
    graph_json = json.dumps(graph)

    html_content = RELATIONSHIP_FINDER_TEMPLATE.format(
        people_datalist_options=people_datalist_options,
        graph_json=graph_json
    )

    with open('relationship.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Generated relationship.html with embedded family graph data")

def generate_interactive_graph_html(gedcom_parser, individuals_data):
    """Generate the interactive_graph.html file with embedded graph data and Topola viewer."""
    graph = build_family_graph(gedcom_parser, individuals_data)

    # Sort individuals by display name for datalist
    sorted_people = sorted(graph.values(), key=lambda p: p['name'])
    datalist_options = []
    for p in sorted_people:
        dates = ""
        if p['birth'] or p['death']:
            b = f"*{p['birth']}" if p['birth'] else ""
            d = f"+{p['death']}" if p['death'] else ""
            dates = f" ({' '.join(filter(None, [b, d]))})"
        val = f"{p['name']}{dates} [{p['id']}]"
        datalist_options.append(f'                <option value="{escape_text(val)}"></option>')

    people_datalist_options = "\n".join(datalist_options)
    graph_json = json.dumps(graph)

    # Read the raw GEDCOM file content
    gedcom_content = ""
    if os.path.exists(GEDCOM_FILE):
        with open(GEDCOM_FILE, 'r', encoding='utf-8') as gf:
            gedcom_content = gf.read()

    html_content = (
        INTERACTIVE_GRAPH_TEMPLATE
        .replace('__PEOPLE_DATALIST_OPTIONS__', people_datalist_options)
        .replace('__GRAPH_JSON__', graph_json)
        .replace('__GEDCOM_CONTENT__', gedcom_content)
    )

    with open('interactive_graph.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Generated interactive_graph.html with native Topola viewer")

def generate_pedigree_section(gedcom_parser, element, individual_id, individuals_data):
    """Generate the HTML for the pedigree section."""
    name = escape_text(get_name(element))

    # Get families information
    families_info = get_families(gedcom_parser, element)
    if not families_info:
        return ""

    # Start with the current individual
    pedigree_content = f'<li class="thisperson">\n            {name}'

    # Add spouses and children if any
    spouses_list = []
    for family in families_info:
        husband = family['husband']
        wife = family['wife']
        children = family['children']

        # Determine spouse based on individual's gender
        individual_gender = get_gender(element)
        if individual_gender == "male":
            spouse = wife
        else:
            spouse = husband

        # Skip only families with neither a spouse nor any children
        if not spouse and not children:
            continue

        # Create spouse entry (unlinked "Unknown" when spouse is unrecorded)
        if spouse:
            spouse_id = generate_id_from_pointer(spouse.get_pointer())
            spouse_path = get_path_for_individual(spouse_id, individuals_data)
            spouse_name_esc = escape_text(get_name(spouse))
            spouse_entry = f'<li class="spouse">\n                    <a href="../../{spouse_path}">{spouse_name_esc}</a>'
        else:
            spouse_entry = '<li class="spouse">\n                    Unknown'

        # Add children if any
        if children:
            children_list = []
            for child in children:
                child_id = generate_id_from_pointer(child.get_pointer())
                child_path = get_path_for_individual(child_id, individuals_data)
                child_name = escape_text(get_name(child))

                children_list.append(f'<li>\n                            <a href="../../{child_path}">{child_name}</a>\n                        </li>')

            if children_list:
                spouse_entry += '<ol>' + ''.join(children_list) + '</ol>'

        spouse_entry += '</li>'
        spouses_list.append(spouse_entry)

    # Add spouses list if any
    if spouses_list:
        pedigree_content += '<ol class="spouselist">' + ''.join(spouses_list) + '</ol>'

    pedigree_content += '</li>'

    return PEDIGREE_TEMPLATE.format(pedigree_content=pedigree_content)

ANCESTOR_SLOTS = [
    {'path': ('father',), 'gender': 'male', 'col': 1, 'block_indent': '        '},
    {'path': ('father', 'father'), 'gender': 'male', 'col': 2, 'block_indent': '            '},
    {'path': ('father', 'father', 'father'), 'gender': 'male', 'col': 3, 'block_indent': '                '},
    {'path': ('father', 'father', 'mother'), 'gender': 'female', 'col': 3, 'block_indent': '                '},
    {'path': ('father', 'mother'), 'gender': 'female', 'col': 2, 'block_indent': '            '},
    {'path': ('father', 'mother', 'father'), 'gender': 'male', 'col': 3, 'block_indent': '                '},
    {'path': ('father', 'mother', 'mother'), 'gender': 'female', 'col': 3, 'block_indent': '                '},
    {'path': ('mother',), 'gender': 'female', 'col': 1, 'block_indent': '        '},
    {'path': ('mother', 'father'), 'gender': 'male', 'col': 2, 'block_indent': '            '},
    {'path': ('mother', 'father', 'father'), 'gender': 'male', 'col': 3, 'block_indent': '                '},
    {'path': ('mother', 'father', 'mother'), 'gender': 'female', 'col': 3, 'block_indent': '                '},
    {'path': ('mother', 'mother'), 'gender': 'female', 'col': 2, 'block_indent': '            '},
    {'path': ('mother', 'mother', 'father'), 'gender': 'male', 'col': 3, 'block_indent': '                '},
    {'path': ('mother', 'mother', 'mother'), 'gender': 'female', 'col': 3, 'block_indent': '                '},
]

COL_BOX_LEFT = {0: 6, 1: 316, 2: 626, 3: 936}
COL_SHADOW_LEFT = {0: 10, 1: 320, 2: 630, 3: 940}
COL_INLINE_LEFT = {0: 285, 1: 595, 2: 905}
COL_BRANCH_LEFT = {1: 300, 2: 610, 3: 920}


def compute_ancestor_layout(present_paths, slot_height=80, gap=40, single_offset=60):
    """
    Compute an adaptive, compact vertical and horizontal layout for the ancestor tree
    based on which ancestor paths are actually present.

    Returns:
        tuple: (box_tops_dict, container_width, container_height)
    """
    present = set(present_paths)
    present.add(())

    def get_subtree_layout(path):
        f_path = path + ('father',)
        m_path = path + ('mother',)
        has_f = f_path in present
        has_m = m_path in present

        if not has_f and not has_m:
            return {path: 0.0}, float(slot_height)

        if has_f and has_m:
            f_pos, f_h = get_subtree_layout(f_path)
            m_pos, m_h = get_subtree_layout(m_path)

            offset_m = f_h + gap
            pos = {}
            for k, v in f_pos.items():
                pos[k] = v
            for k, v in m_pos.items():
                pos[k] = v + offset_m

            pos[path] = (pos[f_path] + pos[m_path]) / 2.0
            total_h = f_h + gap + m_h
            return pos, total_h

        if has_f:
            f_pos, _ = get_subtree_layout(f_path)
            pos = dict(f_pos)
            pos[path] = pos[f_path] + single_offset
            min_y = min(pos.values())
            if min_y < 0:
                for k in pos:
                    pos[k] -= min_y
            max_y = max(v + slot_height for v in pos.values())
            return pos, max_y

        # only has_m
        m_pos, _ = get_subtree_layout(m_path)
        pos = dict(m_pos)
        pos[path] = pos[m_path] - single_offset
        min_y = min(pos.values())
        if min_y < 0:
            for k in pos:
                pos[k] -= min_y
        max_y = max(v + slot_height for v in pos.values())
        return pos, max_y

    raw_pos, _ = get_subtree_layout(())
    top_padding = 5
    box_tops = {k: int(round(v + top_padding)) for k, v in raw_pos.items()}
    max_col = max((len(k) for k in present), default=1)
    container_width = {1: 620, 2: 930, 3: 1234}.get(max_col, 1234)
    max_bottom = max(top + slot_height for top in box_tops.values())
    container_height = max_bottom + 25
    return box_tops, container_width, container_height


def generate_ancestors_section(gedcom_parser, element, individual_id, individuals_data):
    """Generate the HTML for the ancestors section using adaptive subtree layout."""
    name = escape_text(get_name(element))
    birth_date = escape_text(get_birth_data(element))
    death_date = escape_text(get_death_data(element))
    gender_class = "male" if get_gender(element) == "male" else "female"

    # Get parents information
    parents_info = get_parents(gedcom_parser, element)

    # If no parents, return empty string
    if not parents_info or (not parents_info['father'] and not parents_info['mother']):
        return ""

    # Resolve ancestors map: relationship path tuple -> IndividualElement
    ancestors_by_path = {}
    if parents_info['father']:
        ancestors_by_path[('father',)] = parents_info['father']
    if parents_info['mother']:
        ancestors_by_path[('mother',)] = parents_info['mother']

    for slot in ANCESTOR_SLOTS:
        path = slot['path']
        if len(path) == 1:
            continue
        parent_path = path[:-1]
        relation = path[-1]
        if parent_path in ancestors_by_path:
            parent_elem = ancestors_by_path[parent_path]
            p_info = get_parents(gedcom_parser, parent_elem)
            if p_info and p_info.get(relation):
                ancestors_by_path[path] = p_info[relation]

    box_tops, container_width, container_height = compute_ancestor_layout(ancestors_by_path.keys())
    self_top = box_tops[()]
    self_shadow_top = self_top + 5

    # Start with the current individual
    ancestors_content = f'''
    <div id="treeContainer" style="width:{container_width}px; height:{container_height}px; top: 0px">
    <div class="boxbg {gender_class} AncCol0" style="top: {self_top}px; left: 6px;">
        <a class="noThumb" href="../../{get_path_for_individual(individual_id, individuals_data)}">
        {name}<br/>*{birth_date or ''}<br/>+{death_date or '...'}
        </a>
    </div>
    <div class="shadow" style="top: {self_shadow_top}px; left: 10px;"></div>
    '''

    emitted_inlines = set()

    # Render each present ancestor slot in order
    for slot in ANCESTOR_SLOTS:
        path = slot['path']
        if path not in ancestors_by_path:
            continue
        person = ancestors_by_path[path]
        pid = generate_id_from_pointer(person.get_pointer())
        p_path = get_path_for_individual(pid, individuals_data)
        p_name = escape_text(get_name(person))
        p_birth = escape_text(get_birth_data(person))
        p_death = escape_text(get_death_data(person))

        col = slot['col']
        box_top = box_tops[path]
        box_left = COL_BOX_LEFT[col]
        shadow_top = box_top + 5
        shadow_left = COL_SHADOW_LEFT[col]
        bvline_top = box_top + 20
        bvline_left = COL_BRANCH_LEFT[col]

        parent_path = path[:-1]
        parent_top = box_tops[parent_path]
        parent_anchor = parent_top + 20

        if path[-1] == 'father':
            bhline_top = bvline_top
            bhline_height = (parent_anchor - bvline_top) + 1
        else:
            bhline_top = parent_anchor
            bhline_height = (bvline_top - parent_anchor) + 1

        indent = slot['block_indent']
        sub_indent = indent + '    '

        block = ""
        if parent_path not in emitted_inlines:
            emitted_inlines.add(parent_path)
            inline_left = COL_INLINE_LEFT[col - 1]
            inline_top = parent_anchor
            inline_gv_top = parent_anchor + 5
            block += f'''
{indent}<div class="bvline" style="top: {inline_top}px; left: {inline_left}px; width: 15px"></div>
{indent}<div class="gvline" style="top: {inline_gv_top}px; left: {inline_left}px; width: 20px"></div>'''

        block += f'''
{indent}<div class="boxbg {slot['gender']} AncCol{col}" style="top: {box_top}px; left: {box_left}px;">
{sub_indent}<a class="noThumb" href="../../{p_path}">
{sub_indent}{p_name}<br/>*{p_birth or ''}<br/>+{p_death or '...'}
{sub_indent}</a>
{indent}</div>
{indent}<div class="shadow" style="top: {shadow_top}px; left: {shadow_left}px;"></div>
{indent}<div class="bvline" style="top: {bvline_top}px; left: {bvline_left}px; width: 15px;"></div>
{indent}<div class="bhline" style="top: {bhline_top}px; left: {bvline_left}px; height: {bhline_height}px;"></div>
{indent}'''
        ancestors_content += block

    return ANCESTORS_TEMPLATE.format(ancestors_content=ancestors_content)
