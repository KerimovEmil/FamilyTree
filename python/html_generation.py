#!/usr/bin/env python3
"""
Functions for generating HTML content from GEDCOM data with new directory structure.
"""

import os
from datetime import datetime
from utils import generate_id_from_pointer
from data_extraction import (
    get_name, get_gender, get_birth_data, get_death_data, get_parents, get_families
)
from constants import (
    HTML_TEMPLATE, PARENTS_TEMPLATE,
    PARENT_ROW_TEMPLATE, SIBLING_ROW_TEMPLATE, FAMILIES_TEMPLATE,
    FAMILY_ROW_TEMPLATE, CHILD_ROW_TEMPLATE, PEDIGREE_TEMPLATE,
    ANCESTORS_TEMPLATE, INDEX_HTML_TEMPLATE, INDIVIDUALS_HTML_TEMPLATE,
    SURNAME_ENTRY_TEMPLATE, INDIVIDUAL_ENTRY_TEMPLATE, SURNAME_PAGE_TEMPLATE,
    SURNAME_INDIVIDUAL_ENTRY_TEMPLATE, SURNAMES_DIR
)

def extract_name_parts(name):
    """Extract surname and given name from a full name."""
    if ',' in name:
        surname, given_name = name.split(',', 1)
        return surname.strip(), given_name.strip()
    else:
        # Handle cases where there's no comma in the name
        return "Unknown", name

def get_path_for_individual(individual_id, individuals_data):
    """Get the path for an individual using the new structure."""
    if individual_id in individuals_data and 'path' in individuals_data[individual_id]:
        return individuals_data[individual_id]['path']
    else:
        # Fallback to old path structure if not found
        print(f"Warning: Could not find path for individual {individual_id}")
        return f"ppl/{individual_id[0]}/{individual_id[1]}/{individual_id}.html"

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
        father_name = get_name(father)
        father_birth = get_birth_data(father)
        father_death = get_death_data(father)

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
        mother_name = get_name(mother)
        mother_birth = get_birth_data(mother)
        mother_death = get_death_data(mother)

        parents_rows.append(PARENT_ROW_TEMPLATE.format(
            relation="Mother",
            parent_path=mother_path,
            parent_name=mother_name,
            parent_birth=mother_birth,
            parent_death=mother_death
        ))

    # Add self row
    individual_name = get_name(individual)
    individual_birth = get_birth_data(individual)
    individual_death = get_death_data(individual)

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
        sibling_name = get_name(sibling)
        sibling_birth = get_birth_data(sibling)
        sibling_death = get_death_data(sibling)
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

        # If spouse is None, skip this family
        if not spouse:
            continue

        spouse_id = generate_id_from_pointer(spouse.get_pointer())
        spouse_path = get_path_for_individual(spouse_id, individuals_data)
        spouse_name = get_name(spouse)
        spouse_birth = get_birth_data(spouse)
        spouse_death = get_death_data(spouse)

        # Generate children rows
        children_rows = []
        for child in children:
            child_id = generate_id_from_pointer(child.get_pointer())
            child_path = get_path_for_individual(child_id, individuals_data)
            child_name = get_name(child)
            child_birth = get_birth_data(child)
            child_death = get_death_data(child)

            children_rows.append(CHILD_ROW_TEMPLATE.format(
                child_path=child_path,
                child_name=child_name,
                child_birth=child_birth,
                child_death=child_death
            ))

        # Get husband and wife names for the family title
        husband_name = get_name(husband) if husband else "Unknown"
        wife_name = get_name(wife) if wife else "Unknown"

        families_rows.append(FAMILY_ROW_TEMPLATE.format(
            husband_name=husband_name,
            wife_name=wife_name,
            spouse_relation=spouse_relation,
            spouse_path=spouse_path,
            spouse_name=spouse_name,
            spouse_birth=spouse_birth,
            spouse_death=spouse_death if spouse_death else "...",
            children_rows=''.join(children_rows)
        ))

    return FAMILIES_TEMPLATE.format(families_rows=''.join(families_rows))

def generate_html_for_individual_new_structure(gedcom_parser, element, individuals_data):
    """Generate HTML content for an individual with new path structure."""
    individual_id = generate_id_from_pointer(element.get_pointer())
    name = get_name(element)
    gender = get_gender(element)
    birth_date = get_birth_data(element)
    death_date = get_death_data(element)

    # Generate parents section
    parents_section = generate_parents_section(gedcom_parser, element, individual_id, individuals_data)

    # Generate families section
    families_section = generate_families_section(gedcom_parser, element, individual_id, individuals_data)

    # Generate pedigree section
    pedigree_section = generate_pedigree_section(gedcom_parser, element, individual_id, individuals_data)

    # Generate ancestors section
    ancestors_section = generate_ancestors_section(gedcom_parser, element, individual_id, individuals_data)

    # Get current date for footer
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Fill in the HTML template
    html_content = HTML_TEMPLATE.format(
        name=name,
        gender=gender,
        birth_date=birth_date,
        married_name_section="",
        parents_section=parents_section,
        families_section=families_section,
        attributes_section="",
        pedigree_section=pedigree_section,
        ancestors_section=ancestors_section,
        current_date=current_date
    )

    return html_content

def generate_index_html_new_structure(individuals_data):
    """Generate the index.html file with surname index using new paths."""
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
            given_name = data.get('given_name', '')
            path = data.get('path', '')
            name = data.get('name', '')
            given_names_html += f'<a href="{path}" title="{name}">{given_name}</a>, '

        # Remove trailing comma and space
        given_names_html = given_names_html.rstrip(', ')

        # Get the surname page path
        surname_path = f"surnames/{surname.lower().replace(' ', '_')}.html"

        # Add surname entry
        surname_entries += SURNAME_ENTRY_TEMPLATE.format(
            surname=surname,
            surname_path=surname_path,
            given_names=given_names_html
        )

    # Get current date for footer
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Fill in the template
    html_content = INDEX_HTML_TEMPLATE.format(
        surname_entries=surname_entries,
        current_date=current_date
    )

    # Write to file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Generated index.html with new paths")

def generate_individuals_html_new_structure(individuals_data):
    """Generate the individuals.html file with all individuals using new paths."""
    # Sort individuals by name
    sorted_individuals = sorted(individuals_data.items(), key=lambda x: x[1]['name'])

    # Generate individual entries
    individual_entries = ""
    for individual_id, data in sorted_individuals:
        name = data.get('name', '')
        birth_date = data.get('birth_date', '')
        death_date = data.get('death_date', '')
        path = data.get('path', '')

        individual_entries += INDIVIDUAL_ENTRY_TEMPLATE.format(
            path=path,
            name=name,
            birth_date=birth_date,
            death_date=death_date
        )

    # Get current date for footer
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Fill in the template
    html_content = INDIVIDUALS_HTML_TEMPLATE.format(
        individual_entries=individual_entries,
        current_date=current_date
    )

    # Write to file
    with open('individuals.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Generated individuals.html with new paths")

def generate_surname_pages_new_structure(individuals_data):
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
            given_name = data.get('given_name', '')
            birth_date = data.get('birth_date', '')
            path = data.get('path', '')

            individual_entries += SURNAME_INDIVIDUAL_ENTRY_TEMPLATE.format(
                path=path,
                given_name=given_name,
                birth_date=birth_date
            )

        # Get current date for footer
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Fill in the template
        html_content = SURNAME_PAGE_TEMPLATE.format(
            surname=surname,
            individual_entries=individual_entries,
            current_date=current_date
        )

        # Create a safe filename
        safe_surname = surname.lower().replace(' ', '_')
        file_path = os.path.join(SURNAMES_DIR, f"{safe_surname}.html")

        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Generated surname page for {surname} at {file_path}")

def generate_pedigree_section(gedcom_parser, element, individual_id, individuals_data):
    """Generate the HTML for the pedigree section."""
    name = get_name(element)

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

        # Skip if no spouse
        if not spouse:
            continue

        spouse_id = generate_id_from_pointer(spouse.get_pointer())
        spouse_path = get_path_for_individual(spouse_id, individuals_data)
        spouse_name = get_name(spouse)

        # Create spouse entry
        spouse_entry = f'<li class="spouse">\n                    <a href="../../../FamilyTree/{spouse_path}">{spouse_name}</a>'

        # Add children if any
        if children:
            children_list = []
            for child in children:
                child_id = generate_id_from_pointer(child.get_pointer())
                child_path = get_path_for_individual(child_id, individuals_data)
                child_name = get_name(child)

                children_list.append(f'<li>\n                            <a href="../../../FamilyTree/{child_path}">{child_name}</a>\n                        </li>')

            if children_list:
                spouse_entry += '<ol>' + ''.join(children_list) + '</ol>'

        spouse_entry += '</li>'
        spouses_list.append(spouse_entry)

    # Add spouses list if any
    if spouses_list:
        pedigree_content += '<ol class="spouselist">' + ''.join(spouses_list) + '</ol>'

    pedigree_content += '</li>'

    return PEDIGREE_TEMPLATE.format(pedigree_content=pedigree_content)

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
    <div id="treeContainer" style="width:614px; height:300px; top: 0px">
    <div class="boxbg {gender_class} AncCol0" style="top: 80px; left: 6px;">
        <a class="noThumb" href="../../{get_path_for_individual(individual_id, individuals_data)}">
        {name}<br/>*{birth_date or ''}<br/>+{death_date or '...'}
        </a>
    </div>
    <div class="shadow" style="top: 85px; left: 10px;"></div>
    '''

    # Add father if available
    if parents_info['father']:
        father = parents_info['father']
        father_id = generate_id_from_pointer(father.get_pointer())
        father_path = get_path_for_individual(father_id, individuals_data)
        father_name = get_name(father)
        father_birth = get_birth_data(father)
        father_death = get_death_data(father)

        ancestors_content += f'''
        <div class="bvline" style="top: 100px; left: 285px; width: 15px"></div>
        <div class="gvline" style="top: 105px; left: 285px; width: 20px"></div>

        <div class="boxbg male AncCol1" style="top: 5px; left: 316px;">
            <a class="noThumb" href="../../../FamilyTree/{father_path}">
            {father_name}<br/>*{father_birth or ''}<br/>+{father_death or '...'}
            </a>
        </div>
        <div class="shadow" style="top: 10px; left: 320px;"></div>
        '''

    # Add mother if available
    if parents_info['mother']:
        mother = parents_info['mother']
        mother_id = generate_id_from_pointer(mother.get_pointer())
        mother_path = get_path_for_individual(mother_id, individuals_data)
        mother_name = get_name(mother)
        mother_birth = get_birth_data(mother)
        mother_death = get_death_data(mother)

        ancestors_content += f'''
        <div class="bvline" style="top: 100px; left: 285px; width: 15px"></div>
        <div class="pvline" style="top: 105px; left: 285px; width: 20px"></div>

        <div class="boxbg female AncCol1" style="top: 155px; left: 316px;">
            <a class="noThumb" href="../../../FamilyTree/{mother_path}">
            {mother_name}<br/>*{mother_birth or ''}<br/>+{mother_death or '...'}
            </a>
        </div>
        <div class="shadow" style="top: 160px; left: 320px;"></div>
        '''

    return ANCESTORS_TEMPLATE.format(ancestors_content=ancestors_content)
