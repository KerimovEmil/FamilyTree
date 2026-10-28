#!/usr/bin/env python3
"""
Functions for extracting data from GEDCOM elements.
"""

import re

MONTH_MAP = {
    'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
    'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
}


def parse_date(date_str):
    """
    Parse a GEDCOM date string into (year, month, day, is_exact).
    Returns None if no year could be extracted.
    """
    if not date_str:
        return None
    date_str = str(date_str).strip()
    m = re.search(r'(\d{1,2})\s+([A-Za-z]{3})\s+(\d{3,4})', date_str)
    if m and m.group(2).upper() in MONTH_MAP:
        day = int(m.group(1))
        mon = MONTH_MAP[m.group(2).upper()]
        year = int(m.group(3))
        return (year, mon, day, True)
    m = re.search(r'\b([A-Za-z]{3})\s+(\d{3,4})', date_str)
    if m and m.group(1).upper() in MONTH_MAP:
        mon = MONTH_MAP[m.group(1).upper()]
        year = int(m.group(2))
        return (year, mon, 1, False)
    m = re.search(r'\b(\d{3,4})\b', date_str)
    if m:
        year = int(m.group(1))
        return (year, 0, 0, False)
    return None


def calculate_age(birth_date_str, event_date_str):
    """
    Calculate age (in years) between birth and a given event.
    Returns formatted age string (e.g. '50', '83') or '' if cannot be computed.
    """
    b = parse_date(birth_date_str)
    e = parse_date(event_date_str)
    if not b or not e:
        return ""
    b_yr, b_mo, b_dy, b_exact = b
    e_yr, e_mo, e_dy, e_exact = e
    if e_yr < b_yr:
        return ""
    if b_exact and e_exact and b_mo > 0 and e_mo > 0:
        age = e_yr - b_yr - (1 if (e_mo, e_dy) < (b_mo, b_dy) else 0)
        return str(age)
    else:
        diff = e_yr - b_yr
        return str(diff)



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
    """Extract birth date from an individual element."""
    birth_data = individual.get_birth_data()
    birth_date = ""

    if birth_data:
        # The python-gedcom library returns a tuple (date, place, sources)
        if isinstance(birth_data, tuple):
            if birth_data[0]:  # date
                birth_date = birth_data[0]
        # For backward compatibility, also handle dictionary format
        elif isinstance(birth_data, dict):
            if 'date' in birth_data:
                birth_date = birth_data['date']

    return birth_date

def get_birth_place(individual):
    """Extract birth place from an individual element."""
    birth_data = individual.get_birth_data()
    birth_place = ""

    if birth_data:
        if isinstance(birth_data, tuple) and len(birth_data) > 1 and birth_data[1]:
            birth_place = birth_data[1]
        elif isinstance(birth_data, dict) and 'place' in birth_data and birth_data['place']:
            birth_place = birth_data['place']

    return birth_place

def get_death_data(individual):
    """Extract death date from an individual element."""
    death_data = individual.get_death_data()
    death_date = ""

    if death_data:
        # The python-gedcom library returns a tuple (date, place, sources)
        if isinstance(death_data, tuple):
            if death_data[0]:  # date
                death_date = death_data[0]
        # For backward compatibility, also handle dictionary format
        elif isinstance(death_data, dict):
            if 'date' in death_data:
                death_date = death_data['date']

    return death_date

def get_death_place(individual):
    """Extract death place from an individual element."""
    death_data = individual.get_death_data()
    death_place = ""

    if death_data:
        if isinstance(death_data, tuple) and len(death_data) > 1 and death_data[1]:
            death_place = death_data[1]
        elif isinstance(death_data, dict) and 'place' in death_data and death_data['place']:
            death_place = death_data['place']

    return death_place

def has_death_event(individual):
    """Check if individual has a recorded death event (dated, placed, or flagged)."""
    death_data = individual.get_death_data()
    if death_data:
        if isinstance(death_data, tuple) and (death_data[0] or (len(death_data) > 1 and death_data[1])):
            return True
        elif isinstance(death_data, dict) and ('date' in death_data or 'place' in death_data):
            return True
    for child in individual.get_child_elements():
        if child.get_tag() == "DEAT":
            return True
    return False

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

def _extract_full_text(element):
    """Reconstruct multi-line text from an element with CONT and CONC children."""
    text = element.get_value() or ""
    for child in element.get_child_elements():
        tag = child.get_tag()
        val = child.get_value() or ""
        if tag == "CONT":
            text += "\n" + val
        elif tag == "CONC":
            text += val
    return text.strip()

def get_notes(gedcom_parser, individual):
    """Extract notes for an individual, resolving both @N...@ pointers and inline notes."""
    if not individual:
        return []

    note_map = {}
    if gedcom_parser:
        for root_el in gedcom_parser.get_root_child_elements():
            if root_el.get_tag() == "NOTE" and root_el.get_pointer():
                note_map[root_el.get_pointer()] = _extract_full_text(root_el)

    notes = []
    for child in individual.get_child_elements():
        if child.get_tag() == "NOTE":
            val = (child.get_value() or "").strip()
            if val.startswith("@") and val.endswith("@"):
                resolved = note_map.get(val, "")
                if resolved and not resolved.startswith("Records not imported"):
                    notes.append(resolved)
            else:
                inline_text = _extract_full_text(child)
                if inline_text and not inline_text.startswith("Records not imported"):
                    notes.append(inline_text)

    return notes

def get_photos(individual):
    """Extract photo file paths (OBJE -> FILE) for an individual."""
    if not individual:
        return []

    photos = []
    for child in individual.get_child_elements():
        if child.get_tag() == "OBJE":
            for sub in child.get_child_elements():
                if sub.get_tag() == "FILE":
                    val = (sub.get_value() or "").strip()
                    if val:
                        photos.append(val)
    return photos

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
