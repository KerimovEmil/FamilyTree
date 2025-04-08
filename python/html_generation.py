#!/usr/bin/env python3
"""
Functions for generating HTML content from GEDCOM data.
"""

import os
from datetime import datetime
from utils import generate_id_from_pointer, get_relative_path, get_surname_file_path, get_surname_relative_path
from data_extraction import (
    get_name, get_gender, get_birth_data, get_death_data, get_occupation,
    get_attributes, get_parents, get_families
)
from constants import (
    HTML_TEMPLATE, DEATH_TEMPLATE, OCCUPATION_TEMPLATE, PARENTS_TEMPLATE,
    PARENT_ROW_TEMPLATE, SIBLING_ROW_TEMPLATE, FAMILIES_TEMPLATE,
    FAMILY_ROW_TEMPLATE, CHILD_ROW_TEMPLATE, PEDIGREE_TEMPLATE,
    ANCESTORS_TEMPLATE, INDEX_HTML_TEMPLATE, INDIVIDUALS_HTML_TEMPLATE,
    SURNAME_ENTRY_TEMPLATE, INDIVIDUAL_ENTRY_TEMPLATE, SURNAME_PAGE_TEMPLATE,
    SURNAME_INDIVIDUAL_ENTRY_TEMPLATE, SURNAMES_DIR
)

def generate_parents_section(gedcom_parser, individual, individual_id):
    """Generate the HTML for the parents section."""
    parents_info = get_parents(gedcom_parser, individual)
    if not parents_info:
        return ""

    parents_rows = []

    # Add father row
    if parents_info['father']:
        father = parents_info['father']
        father_id = generate_id_from_pointer(father.get_pointer())
        father_path = get_relative_path(father_id)
        father_name = get_name(father)
        father_birth, _ = get_birth_data(father)
        father_death, _ = get_death_data(father)

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
        mother_path = get_relative_path(mother_id)
        mother_name = get_name(mother)
        mother_birth, _ = get_birth_data(mother)
        mother_death, _ = get_death_data(mother)

        parents_rows.append(PARENT_ROW_TEMPLATE.format(
            relation="Mother",
            parent_path=mother_path,
            parent_name=mother_name,
            parent_birth=mother_birth,
            parent_death=mother_death
        ))

    # Add self row
    individual_name = get_name(individual)
    individual_birth, _ = get_birth_data(individual)
    individual_death, _ = get_death_data(individual)

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
        sibling_path = get_relative_path(sibling_id)
        sibling_name = get_name(sibling)
        sibling_birth, _ = get_birth_data(sibling)
        sibling_death, _ = get_death_data(sibling)
        sibling_gender = get_gender(sibling)

        relation = "Sister" if sibling_gender == "female" else "Brother"

        sibling_link = f'<a href="../../../{sibling_path}">{sibling_name}</a>'

        parents_rows.append(SIBLING_ROW_TEMPLATE.format(
            relation=relation,
            sibling_link=sibling_link,
            sibling_birth=sibling_birth,
            sibling_death=sibling_death
        ))

    return PARENTS_TEMPLATE.format(parents_rows=''.join(parents_rows))

def generate_families_section(gedcom_parser, individual, individual_id):
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
        spouse_path = get_relative_path(spouse_id)
        spouse_name = get_name(spouse)
        spouse_birth, _ = get_birth_data(spouse)
        spouse_death, _ = get_death_data(spouse)

        # Generate children rows
        children_rows = []
        for child in children:
            child_id = generate_id_from_pointer(child.get_pointer())
            child_path = get_relative_path(child_id)
            child_name = get_name(child)
            child_birth, _ = get_birth_data(child)
            child_death, _ = get_death_data(child)

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

def generate_pedigree_section(gedcom_parser, individual, individual_id):
    """Generate a pedigree section showing ancestors and descendants."""
    # Get parents information
    parents_info = get_parents(gedcom_parser, individual)

    # Get families information (spouses and children)
    families_info = get_families(gedcom_parser, individual)

    # If no parents and no families, return empty string
    if (not parents_info or (not parents_info['father'] and not parents_info['mother'])) and not families_info:
        return ""

    # Get individual details
    name = get_name(individual)

    # Start building the pedigree content
    pedigree_content = ""

    # If we have parents, show the father as the root
    if parents_info and parents_info['father']:
        father = parents_info['father']
        father_id = generate_id_from_pointer(father.get_pointer())
        father_name = get_name(father)
        father_path = get_relative_path(father_id)

        # Start with father
        pedigree_content += f"""<li>
            <a href="../../../{father_path}">{father_name}</a>
            <ol>"""

        # Add mother if available
        if parents_info['mother']:
            mother = parents_info['mother']
            mother_id = generate_id_from_pointer(mother.get_pointer())
            mother_name = get_name(mother)
            mother_path = get_relative_path(mother_id)

            pedigree_content += f"""<li class="spouse">
                <a href="../../../{mother_path}">{mother_name}</a>
                <ol>"""

        # Add this person
        pedigree_content += f"""<li class="thisperson">
            {name}"""
    else:
        # If no parents, start with this person
        pedigree_content += f"""<li class="thisperson">
            {name}"""

    # Add spouses and children if available
    if families_info:
        pedigree_content += """<ol class="spouselist">"""

        for family in families_info:
            spouse = None
            gender = get_gender(individual)

            # Determine spouse based on individual's gender
            if gender == "male":
                spouse = family['wife']
            else:
                spouse = family['husband']

            # If spouse exists, add spouse and children
            if spouse:
                spouse_id = generate_id_from_pointer(spouse.get_pointer())
                spouse_name = get_name(spouse)
                spouse_path = get_relative_path(spouse_id)

                pedigree_content += f"""<li class="spouse">
                    <a href="../../../{spouse_path}">{spouse_name}</a>"""

                # Add children if available
                children = family['children']
                if children:
                    pedigree_content += """<ol>"""

                    for child in children:
                        child_id = generate_id_from_pointer(child.get_pointer())
                        child_name = get_name(child)
                        child_path = get_relative_path(child_id)

                        pedigree_content += f"""<li>
                            <a href="../../../{child_path}">{child_name}</a>
                        </li>"""

                    pedigree_content += """</ol>"""

                pedigree_content += """</li>"""

        pedigree_content += """</ol>"""

    # Close the tags
    if parents_info and parents_info['father'] and parents_info['mother']:
        # Close this person, mother, and father tags
        pedigree_content += """</li></ol></li></ol></li>"""
    elif parents_info and parents_info['father']:
        # Close this person and father tags
        pedigree_content += """</li></ol></li>"""
    else:
        # Close this person tag
        pedigree_content += """</li>"""

    return PEDIGREE_TEMPLATE.format(pedigree_content=pedigree_content)

def generate_ancestors_section(gedcom_parser, individual, individual_id):
    """Generate an ancestors tree section."""
    parents_info = get_parents(gedcom_parser, individual)
    if not parents_info or (not parents_info['father'] and not parents_info['mother']):
        return ""

    # Get individual details
    name = get_name(individual)
    birth_date, _ = get_birth_data(individual)
    death_date, _ = get_death_data(individual)
    gender = get_gender(individual)
    gender_class = "male" if gender == "male" else "female"

    # Format dates
    birth_display = f"*{birth_date}" if birth_date else "*"
    death_display = f"+{death_date}" if death_date else "+..."

    # Start building the ancestors tree
    ancestors_content = f"""
    <div class="boxbg {gender_class} AncCol0" style="top: 80px; left: 6px;">
        <a class="noThumb" href="../../../{get_relative_path(individual_id)}">
        {name}<br/>{birth_display}<br/>{death_display}
        </a>
    </div>
    <div class="shadow" style="top: 85px; left: 10px;"></div>
    """

    # Add father if available
    father = parents_info['father']
    mother = parents_info['mother']

    # Only add connecting lines if we have at least one parent
    if father or mother:
        ancestors_content += """
        <div class="bvline" style="top: 100px; left: 285px; width: 15px"></div>
        <div class="gvline" style="top: 105px; left: 285px; width: 20px"></div>
        """

    # Add father details
    if father:
        father_id = generate_id_from_pointer(father.get_pointer())
        father_name = get_name(father)
        father_birth, _ = get_birth_data(father)
        father_death, _ = get_death_data(father)

        # Format dates
        father_birth_display = f"*{father_birth}" if father_birth else "*"
        father_death_display = f"+{father_death}" if father_death else "+..."

        ancestors_content += f"""
        <div class="boxbg male AncCol1" style="top: 5px; left: 316px;">
            <a class="noThumb" href="../../../{get_relative_path(father_id)}">
            {father_name}<br/>{father_birth_display}<br/>{father_death_display}
            </a>
        </div>
        <div class="shadow" style="top: 10px; left: 320px;"></div>
        <div class="bvline" style="top: 25px; left: 300px; width: 15px;"></div>
        """

    # Add connecting lines between parents if both exist
    if father and mother:
        ancestors_content += """
        <div class="bhline" style="top: 25px; left: 300px; height: 76px;"></div>
        """

    # Add mother details
    if mother:
        mother_id = generate_id_from_pointer(mother.get_pointer())
        mother_name = get_name(mother)
        mother_birth, _ = get_birth_data(mother)
        mother_death, _ = get_death_data(mother)

        # Format dates
        mother_birth_display = f"*{mother_birth}" if mother_birth else "*"
        mother_death_display = f"+{mother_death}" if mother_death else "+..."

        ancestors_content += f"""
        <div class="boxbg female AncCol1" style="top: 155px; left: 316px;">
            <a class="noThumb" href="../../../{get_relative_path(mother_id)}">
            {mother_name}<br/>{mother_birth_display}<br/>{mother_death_display}
            </a>
        </div>
        <div class="shadow" style="top: 160px; left: 320px;"></div>
        <div class="bvline" style="top: 175px; left: 300px; width: 15px;"></div>
        """

    # Add final connecting line if both parents exist
    if father and mother:
        ancestors_content += """
        <div class="bhline" style="top: 100px; left: 300px; height: 76px;"></div>
        """

    # Set appropriate container width based on number of generations
    container_width = 614 if (father or mother) else 300

    # Wrap the content in the container div
    ancestors_content = f'<div id="treeContainer" style="width:{container_width}px; height:300px; top: 0px">{ancestors_content}</div>'

    return ANCESTORS_TEMPLATE.format(ancestors_content=ancestors_content)

def generate_html_for_individual(gedcom_parser, individual):
    """Generate HTML content for an individual."""
    individual_id = generate_id_from_pointer(individual.get_pointer())
    name = get_name(individual)
    gender = get_gender(individual)
    birth_date, birth_place = get_birth_data(individual)
    death_date, death_place = get_death_data(individual)
    occupation = get_occupation(individual)

    # Generate death section if applicable
    death_section = ""
    if death_date:
        death_section = DEATH_TEMPLATE.format(
            death_date=death_date,
            death_place=death_place
        )

    # Generate occupation section if applicable
    occupation_section = ""
    if occupation and occupation != "&nbsp;":
        occupation_section = OCCUPATION_TEMPLATE.format(occupation=occupation)

    # Generate married name section if applicable
    married_name_section = ""
    # This would require more complex logic to determine married names

    # Generate attributes section
    attributes = get_attributes(individual)
    attributes_section = ""
    for attr in attributes:
        attributes_section += f"""
<tr>
    <td class="ColumnType">{attr['type']}</td>
    <td class="ColumnValue">{attr['value']}</td>
    <td class="ColumnNotes"><div>{attr['notes']}</div></td>
    <td class="ColumnSources">{attr['sources']}</td>
</tr>
"""

    # Generate parents section
    parents_section = generate_parents_section(gedcom_parser, individual, individual_id)

    # Generate families section
    families_section = generate_families_section(gedcom_parser, individual, individual_id)

    # Generate pedigree section
    pedigree_section = generate_pedigree_section(gedcom_parser, individual, individual_id)

    # Generate ancestors section
    ancestors_section = generate_ancestors_section(gedcom_parser, individual, individual_id)

    # Get current date for footer
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Fix name format if it's still a tuple string
    if isinstance(name, str) and name.startswith("(") and name.endswith(")"):
        # Try to extract the name from the tuple string
        try:
            # Convert string representation of tuple to actual tuple
            name_tuple = eval(name)
            if isinstance(name_tuple, tuple) and len(name_tuple) == 2:
                given_name, surname = name_tuple
                if surname:
                    name = f"{surname}, {given_name}"
                else:
                    name = given_name
        except:
            # If eval fails, just use the name as is
            pass

    # Fill in the HTML template
    html_content = HTML_TEMPLATE.format(
        name=name,
        gender=gender,
        birth_date=birth_date,
        birth_place=birth_place,
        death_section=death_section,
        occupation_section=occupation_section,
        married_name_section=married_name_section,
        parents_section=parents_section,
        families_section=families_section,
        attributes_section=attributes_section,
        pedigree_section=pedigree_section,
        ancestors_section=ancestors_section,
        current_date=current_date
    )

    return html_content

def generate_surname_pages(individuals_data):
    """Generate HTML files for each surname."""
    # Group individuals by surname
    surnames = {}
    for individual_id, data in individuals_data.items():
        name = data['name']
        if ',' in name:
            surname = name.split(',')[0].strip()
            if surname and surname != '___':
                if surname not in surnames:
                    surnames[surname] = []
                surnames[surname].append((individual_id, data))

    # Create surnames directory if it doesn't exist
    os.makedirs(SURNAMES_DIR, exist_ok=True)

    # Generate a page for each surname
    for surname, individuals in surnames.items():
        # Sort individuals by name
        sorted_individuals = sorted(individuals, key=lambda x: x[1]['name'])

        # Generate individual entries
        individual_entries = ""
        for individual_id, data in sorted_individuals:
            name = data['name']
            # Extract given name from the full name
            given_name = name.split(',')[1].strip() if ',' in name else name
            birth_date = data.get('birth_date', '')
            individual_path = "../" + get_relative_path(individual_id)

            individual_entries += SURNAME_INDIVIDUAL_ENTRY_TEMPLATE.format(
                individual_path=individual_path,
                individual_name=given_name,
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

        # Write to file
        file_path = get_surname_file_path(surname)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Generated surname page for {surname} at {file_path}")

    return surnames

def generate_index_html(individuals_data):
    """Generate the index.html file with surname index."""
    # Generate surname pages first and get the surnames dictionary
    surnames = generate_surname_pages(individuals_data)

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
            name = data['name']
            given_name = name.split(',')[1].strip() if ',' in name else name
            path = get_relative_path(individual_id)
            given_names_html += f'<a href="{path}" title="{name}">{given_name}</a>, '

        # Remove trailing comma and space
        given_names_html = given_names_html.rstrip(', ')

        # Get the surname page path
        surname_path = get_surname_relative_path(surname)

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

    print("Generated index.html")

def generate_individuals_html(individuals_data):
    """Generate the individuals.html file with all individuals."""
    # Sort individuals by name
    sorted_individuals = sorted(individuals_data.items(), key=lambda x: x[1]['name'])

    # Generate individual entries
    individual_entries = ""
    for individual_id, data in sorted_individuals:
        name = data['name']
        birth_date = data.get('birth_date', '')
        death_date = data.get('death_date', '')
        path = get_relative_path(individual_id)

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

    print("Generated individuals.html")
