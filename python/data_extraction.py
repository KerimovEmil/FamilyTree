#!/usr/bin/env python3
"""
Functions for extracting data from GEDCOM elements.
"""

from utils import generate_id_from_pointer, get_relative_path

def get_name(individual):
    """Extract the name from an individual element."""
    name_tuple = individual.get_name()
    if not name_tuple or name_tuple == ("", ""):
        return "Unknown"

    # Handle the case where name_tuple is already a string
    if isinstance(name_tuple, str):
        return name_tuple

    # Handle the case where name_tuple is a tuple
    if isinstance(name_tuple, tuple) and len(name_tuple) == 2:
        given_name, surname = name_tuple
        if surname:
            return f"{surname}, {given_name}"
        else:
            return given_name

    # If we can't parse the name, return it as is
    return str(name_tuple)

def get_gender(individual):
    """Extract the gender from an individual element."""
    gender = individual.get_gender()
    if gender == "M":
        return "male"
    elif gender == "F":
        return "female"
    else:
        return "unknown"

def get_birth_data(individual):
    """Extract birth date and place from an individual element."""
    birth_data = individual.get_birth_data()
    birth_date = ""
    birth_place = "&nbsp;"

    if birth_data:
        # The python-gedcom library returns a tuple (date, place, sources)
        if isinstance(birth_data, tuple) and len(birth_data) >= 2:
            if birth_data[0]:  # date
                birth_date = birth_data[0]
            if birth_data[1]:  # place
                birth_place = birth_data[1]
        # For backward compatibility, also handle dictionary format
        elif isinstance(birth_data, dict):
            if 'date' in birth_data:
                birth_date = birth_data['date']
            if 'place' in birth_data:
                birth_place = birth_data['place']

    return birth_date, birth_place

def get_death_data(individual):
    """Extract death date and place from an individual element."""
    death_data = individual.get_death_data()
    death_date = ""
    death_place = "&nbsp;"

    if death_data:
        # The python-gedcom library returns a tuple (date, place, sources)
        if isinstance(death_data, tuple) and len(death_data) >= 2:
            if death_data[0]:  # date
                death_date = death_data[0]
            if death_data[1]:  # place
                death_place = death_data[1]
        # For backward compatibility, also handle dictionary format
        elif isinstance(death_data, dict):
            if 'date' in death_data:
                death_date = death_data['date']
            if 'place' in death_data:
                death_place = death_data['place']

    return death_date, death_place

def get_occupation(individual):
    """Extract occupation from an individual element."""
    occupation = individual.get_occupation()
    return occupation if occupation else "&nbsp;"

def get_attributes(individual):
    """Extract attributes from an individual element."""
    attributes = []

    # Get RFN if available
    rfn = None
    for child in individual.get_child_elements():
        if child.get_tag() == "RFN":
            rfn = child.get_value()

    if rfn:
        attributes.append({
            'type': 'RFN',
            'value': rfn,
            'notes': '',
            'sources': '&nbsp;'
        })

    return attributes

def get_parents(gedcom_parser, individual):
    """Get parents information for an individual."""
    families = gedcom_parser.get_families(individual, "FAMC")
    if not families:
        return None

    # Get the first family where the individual is a child
    family = families[0]

    # Get parents
    fathers = gedcom_parser.get_family_members(family, "HUSB")
    father = fathers[0] if fathers else None

    mothers = gedcom_parser.get_family_members(family, "WIFE")
    mother = mothers[0] if mothers else None

    # Get siblings
    all_children = gedcom_parser.get_family_members(family, "CHIL")
    siblings = [child for child in all_children if child != individual]

    return {
        'father': father,
        'mother': mother,
        'siblings': siblings
    }

def get_families(gedcom_parser, individual):
    """Get families information for an individual."""
    families = []
    family_elements = gedcom_parser.get_families(individual, "FAMS")

    for family in family_elements:
        husband = None
        wife = None

        # Get husband and wife
        husbands = gedcom_parser.get_family_members(family, "HUSB")
        if husbands:
            husband = husbands[0]

        wives = gedcom_parser.get_family_members(family, "WIFE")
        if wives:
            wife = wives[0]

        # Get children
        children = gedcom_parser.get_family_members(family, "CHIL")

        families.append({
            'husband': husband,
            'wife': wife,
            'children': children
        })

    return families
