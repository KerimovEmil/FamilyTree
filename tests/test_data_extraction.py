import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))

from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement
from data_extraction import (
    get_name,
    get_gender,
    get_birth_data,
    get_birth_place,
    get_death_data,
    get_death_place,
    has_death_event,
    get_occupation,
    get_attributes,
    get_parents,
    get_families,
    parse_date,
    calculate_age,
)


def load_fixture_parser():
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'sample.ged')
    parser = Parser()
    parser.parse_file(fixture_path)
    return parser


def get_individual_by_pointer(parser, pointer):
    for element in parser.get_root_child_elements():
        if isinstance(element, IndividualElement) and element.get_pointer() == pointer:
            return element
    return None


def test_data_extraction_john_doe():
    parser = load_fixture_parser()
    john = get_individual_by_pointer(parser, "@I1@")
    assert john is not None

    assert get_name(john) == "Doe, John"
    assert get_gender(john) == "male"
    assert get_birth_data(john) == "1 JAN 1970"
    assert get_birth_place(john) == "New York, USA"
    assert get_death_data(john) == "1 JAN 2020"
    assert get_death_place(john) == "Boston, USA"
    assert has_death_event(john) is True
    assert get_occupation(john) == "Engineer"

    attrs = get_attributes(john)
    assert len(attrs) == 1
    assert attrs[0]['type'] == "RFN"
    assert attrs[0]['value'] == "12345"


def test_data_extraction_families_and_single_parent():
    parser = load_fixture_parser()
    john = get_individual_by_pointer(parser, "@I1@")
    families = get_families(parser, john)

    # John has 2 families: F1 (with Jane) and F2 (single father of Solo)
    assert len(families) == 2

    # Family 1 with wife Jane
    f1 = families[0]
    assert f1['wife'] is not None
    assert get_name(f1['wife']) == "Smith, Jane"
    assert len(f1['children']) == 1
    assert get_name(f1['children'][0]) == "Doe, Junior"

    # Family 2: single-parent family (wife is None)
    f2 = families[1]
    assert f2['wife'] is None
    assert len(f2['children']) == 1
    assert get_name(f2['children'][0]) == "Doe, Solo"


def test_data_extraction_parents():
    parser = load_fixture_parser()
    junior = get_individual_by_pointer(parser, "@I3@")
    parents = get_parents(parser, junior)

    assert parents is not None
    assert parents['father'] is not None
    assert get_name(parents['father']) == "Doe, John"
    assert parents['mother'] is not None
    assert get_name(parents['mother']) == "Smith, Jane"

    solo = get_individual_by_pointer(parser, "@I4@")
    solo_parents = get_parents(parser, solo)
    assert solo_parents is not None
    assert solo_parents['father'] is not None
    assert get_name(solo_parents['father']) == "Doe, John"
    assert solo_parents['mother'] is None


def test_parse_date():
    assert parse_date("10 NOV 1939") == (1939, 11, 10, True)
    assert parse_date("1 JAN 2020") == (2020, 1, 1, True)
    assert parse_date("MAY 2024") == (2024, 5, 1, False)
    assert parse_date("1971") == (1971, 0, 0, False)
    assert parse_date("ABT 1920") == (1920, 0, 0, False)
    assert parse_date("") is None
    assert parse_date(None) is None
    assert parse_date("Unknown") is None


def test_calculate_age():
    # Exact birthday
    assert calculate_age("1 JAN 1970", "1 JAN 2020") == "50"
    # Before birthday in anniversary year
    assert calculate_age("15 MAY 1970", "10 MAY 2020") == "49"
    # After birthday in anniversary year
    assert calculate_age("15 MAY 1970", "20 MAY 2020") == "50"
    # Approximate years
    assert calculate_age("1939", "2022") == "83"
    assert calculate_age("5 DEC 1939", "25 APR 2005") == "65"
    # Invalid / reverse / missing
    assert calculate_age("1970", "1960") == ""
    assert calculate_age("", "2020") == ""
    assert calculate_age("1970", "") == ""
    assert calculate_age(None, None) == ""
