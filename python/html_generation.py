#!/usr/bin/env python3
"""
Functions for generating HTML content from GEDCOM data with new directory structure.
"""

import html
import os
from utils import (
    generate_id_from_pointer, get_surname_file_path, get_surname_relative_path,
    extract_name_parts
)
from data_extraction import (
    get_name, get_gender, get_birth_data, get_birth_place, get_death_data,
    get_death_place, has_death_event, get_occupation, get_attributes,
    get_parents, get_families
)

def escape_text(val):
    """Safely escape text for interpolation into HTML templates."""
    if val is None:
        return ""
    return html.escape(str(val))

from constants import (
    HTML_TEMPLATE, EVENT_ROW_TEMPLATE, ATTRIBUTES_SECTION_TEMPLATE,
    ATTRIBUTE_ROW_TEMPLATE, PARENTS_TEMPLATE,
    PARENT_ROW_TEMPLATE, SIBLING_ROW_TEMPLATE, FAMILIES_TEMPLATE,
    FAMILY_ROW_TEMPLATE, CHILD_ROW_TEMPLATE, PEDIGREE_TEMPLATE,
    ANCESTORS_TEMPLATE, INDEX_HTML_TEMPLATE, INDIVIDUALS_HTML_TEMPLATE,
    SURNAME_ENTRY_TEMPLATE, INDIVIDUAL_ENTRY_TEMPLATE, SURNAME_PAGE_TEMPLATE,
    SURNAME_INDIVIDUAL_ENTRY_TEMPLATE, SURNAMES_DIR
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
    """Generate rows for the Events table (Birth, Death, Occupation if applicable)."""
    events_rows = []

    # Birth event
    birth_date = escape_text(get_birth_data(element))
    birth_place = escape_text(get_birth_place(element))
    events_rows.append(EVENT_ROW_TEMPLATE.format(
        event_name="Birth",
        event_date=birth_date,
        event_place=birth_place
    ))

    # Death event
    if has_death_event(element):
        death_date = escape_text(get_death_data(element))
        death_place = escape_text(get_death_place(element))
        events_rows.append(EVENT_ROW_TEMPLATE.format(
            event_name="Death",
            event_date=death_date,
            event_place=death_place
        ))

    # Occupation event
    occupation = get_occupation(element)
    if occupation and occupation.strip() and occupation != "&nbsp;":
        events_rows.append(EVENT_ROW_TEMPLATE.format(
            event_name="Occupation",
            event_date="",
            event_place=escape_text(occupation)
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

def generate_html_for_individual(gedcom_parser, element, individuals_data):
    """Generate HTML content for an individual"""
    individual_id = generate_id_from_pointer(element.get_pointer())
    name = escape_text(get_name(element))
    gender = escape_text(get_gender(element))

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
    {
        'path': ('father',),
        'gender': 'male',
        'col': 1,
        'has_inlines': True,
        'inline_top': 550,
        'inline_left': 285,
        'inline_gv_top': 555,
        'box_top': 230,
        'box_left': 316,
        'shadow_top': 235,
        'shadow_left': 320,
        'bvline_top': 250,
        'bvline_left': 300,
        'bhline_top': 250,
        'bhline_left': 300,
        'bhline_height': 301,
        'block_indent': '        ',
    },
    {
        'path': ('father', 'father'),
        'gender': 'male',
        'col': 2,
        'has_inlines': True,
        'inline_top': 250,
        'inline_left': 595,
        'inline_gv_top': 255,
        'box_top': 80,
        'box_left': 626,
        'shadow_top': 85,
        'shadow_left': 630,
        'bvline_top': 100,
        'bvline_left': 610,
        'bhline_top': 100,
        'bhline_left': 610,
        'bhline_height': 151,
        'block_indent': '            ',
    },
    {
        'path': ('father', 'father', 'father'),
        'gender': 'male',
        'col': 3,
        'has_inlines': True,
        'inline_top': 100,
        'inline_left': 905,
        'inline_gv_top': 105,
        'box_top': 5,
        'box_left': 936,
        'shadow_top': 10,
        'shadow_left': 940,
        'bvline_top': 25,
        'bvline_left': 920,
        'bhline_top': 25,
        'bhline_left': 920,
        'bhline_height': 76,
        'block_indent': '                ',
    },
    {
        'path': ('father', 'father', 'mother'),
        'gender': 'female',
        'col': 3,
        'has_inlines': False,
        'box_top': 155,
        'box_left': 936,
        'shadow_top': 160,
        'shadow_left': 940,
        'bvline_top': 175,
        'bvline_left': 920,
        'bhline_top': 100,
        'bhline_left': 920,
        'bhline_height': 76,
        'block_indent': '                ',
    },
    {
        'path': ('father', 'mother'),
        'gender': 'female',
        'col': 2,
        'has_inlines': False,
        'box_top': 380,
        'box_left': 626,
        'shadow_top': 385,
        'shadow_left': 630,
        'bvline_top': 400,
        'bvline_left': 610,
        'bhline_top': 250,
        'bhline_left': 610,
        'bhline_height': 151,
        'block_indent': '            ',
    },
    {
        'path': ('father', 'mother', 'father'),
        'gender': 'male',
        'col': 3,
        'has_inlines': True,
        'inline_top': 400,
        'inline_left': 905,
        'inline_gv_top': 405,
        'box_top': 305,
        'box_left': 936,
        'shadow_top': 310,
        'shadow_left': 940,
        'bvline_top': 325,
        'bvline_left': 920,
        'bhline_top': 325,
        'bhline_left': 920,
        'bhline_height': 76,
        'block_indent': '                ',
    },
    {
        'path': ('father', 'mother', 'mother'),
        'gender': 'female',
        'col': 3,
        'has_inlines': False,
        'box_top': 455,
        'box_left': 936,
        'shadow_top': 460,
        'shadow_left': 940,
        'bvline_top': 475,
        'bvline_left': 920,
        'bhline_top': 400,
        'bhline_left': 920,
        'bhline_height': 76,
        'block_indent': '                ',
    },
    {
        'path': ('mother',),
        'gender': 'female',
        'col': 1,
        'has_inlines': False,
        'box_top': 830,
        'box_left': 316,
        'shadow_top': 835,
        'shadow_left': 320,
        'bvline_top': 850,
        'bvline_left': 300,
        'bhline_top': 550,
        'bhline_left': 300,
        'bhline_height': 301,
        'block_indent': '        ',
    },
    {
        'path': ('mother', 'father'),
        'gender': 'male',
        'col': 2,
        'has_inlines': True,
        'inline_top': 850,
        'inline_left': 595,
        'inline_gv_top': 855,
        'box_top': 680,
        'box_left': 626,
        'shadow_top': 685,
        'shadow_left': 630,
        'bvline_top': 700,
        'bvline_left': 610,
        'bhline_top': 700,
        'bhline_left': 610,
        'bhline_height': 151,
        'block_indent': '            ',
    },
    {
        'path': ('mother', 'father', 'father'),
        'gender': 'male',
        'col': 3,
        'has_inlines': True,
        'inline_top': 700,
        'inline_left': 905,
        'inline_gv_top': 705,
        'box_top': 605,
        'box_left': 936,
        'shadow_top': 610,
        'shadow_left': 940,
        'bvline_top': 625,
        'bvline_left': 920,
        'bhline_top': 625,
        'bhline_left': 920,
        'bhline_height': 76,
        'block_indent': '                ',
    },
    {
        'path': ('mother', 'father', 'mother'),
        'gender': 'female',
        'col': 3,
        'has_inlines': False,
        'box_top': 755,
        'box_left': 936,
        'shadow_top': 760,
        'shadow_left': 940,
        'bvline_top': 775,
        'bvline_left': 920,
        'bhline_top': 700,
        'bhline_left': 920,
        'bhline_height': 76,
        'block_indent': '                ',
    },
    {
        'path': ('mother', 'mother'),
        'gender': 'female',
        'col': 2,
        'has_inlines': False,
        'box_top': 980,
        'box_left': 626,
        'shadow_top': 985,
        'shadow_left': 630,
        'bvline_top': 1000,
        'bvline_left': 610,
        'bhline_top': 850,
        'bhline_left': 610,
        'bhline_height': 151,
        'block_indent': '            ',
    },
    {
        'path': ('mother', 'mother', 'father'),
        'gender': 'male',
        'col': 3,
        'has_inlines': True,
        'inline_top': 1000,
        'inline_left': 905,
        'inline_gv_top': 1005,
        'box_top': 905,
        'box_left': 936,
        'shadow_top': 910,
        'shadow_left': 940,
        'bvline_top': 925,
        'bvline_left': 920,
        'bhline_top': 925,
        'bhline_left': 920,
        'bhline_height': 76,
        'block_indent': '                ',
    },
    {
        'path': ('mother', 'mother', 'mother'),
        'gender': 'female',
        'col': 3,
        'has_inlines': False,
        'box_top': 1055,
        'box_left': 936,
        'shadow_top': 1060,
        'shadow_left': 940,
        'bvline_top': 1075,
        'bvline_left': 920,
        'bhline_top': 1000,
        'bhline_left': 920,
        'bhline_height': 76,
        'block_indent': '                ',
    },
]

def generate_ancestors_section(gedcom_parser, element, individual_id, individuals_data):
    """Generate the HTML for the ancestors section."""
    name = get_name(element)
    birth_date = get_birth_data(element)
    death_date = get_death_data(element)
    gender_class = "male" if get_gender(element) == "male" else "female"

    # Get parents information
    parents_info = get_parents(gedcom_parser, element)

    # If no parents, return empty string
    if not parents_info or (not parents_info['father'] and not parents_info['mother']):
        return ""

    # Start with the current individual
    ancestors_content = f'''
    <div id="treeContainer" style="width:1234px; height:1200px; top: 0px">
    <div class="boxbg {gender_class} AncCol0" style="top: 530px; left: 6px;">
        <a class="noThumb" href="../../{get_path_for_individual(individual_id, individuals_data)}">
        {name}<br/>*{birth_date or ''}<br/>+{death_date or '...'}
        </a>
    </div>
    <div class="shadow" style="top: 535px; left: 10px;"></div>
    '''

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

        indent = slot['block_indent']
        sub_indent = indent + '    '

        block = ""
        if slot['has_inlines']:
            block += f'''
{indent}<div class="bvline" style="top: {slot['inline_top']}px; left: {slot['inline_left']}px; width: 15px"></div>
{indent}<div class="gvline" style="top: {slot['inline_gv_top']}px; left: {slot['inline_left']}px; width: 20px"></div>'''

        block += f'''
{indent}<div class="boxbg {slot['gender']} AncCol{slot['col']}" style="top: {slot['box_top']}px; left: {slot['box_left']}px;">
{sub_indent}<a class="noThumb" href="../../{p_path}">
{sub_indent}{p_name}<br/>*{p_birth or ''}<br/>+{p_death or '...'}
{sub_indent}</a>
{indent}</div>
{indent}<div class="shadow" style="top: {slot['shadow_top']}px; left: {slot['shadow_left']}px;"></div>
{indent}<div class="bvline" style="top: {slot['bvline_top']}px; left: {slot['bvline_left']}px; width: 15px;"></div>
{indent}<div class="bhline" style="top: {slot['bhline_top']}px; left: {slot['bhline_left']}px; height: {slot['bhline_height']}px;"></div>
{indent}'''
        ancestors_content += block

    return ANCESTORS_TEMPLATE.format(ancestors_content=ancestors_content)
