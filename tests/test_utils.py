import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))

from utils import (
    generate_id_from_pointer,
    extract_name_parts,
    get_surname_file_path,
    get_surname_relative_path,
    get_individual_file_path,
    get_individual_relative_path,
)


def test_generate_id_from_pointer():
    pointer1 = "@I0001@"
    pointer2 = "@I0002@"
    id1 = generate_id_from_pointer(pointer1)
    id2 = generate_id_from_pointer(pointer2)

    assert isinstance(id1, str)
    assert len(id1) == 30
    assert id1 != id2
    # Deterministic
    assert id1 == generate_id_from_pointer(pointer1)


def test_extract_name_parts():
    # Standard Surname, Given Name
    surname, given = extract_name_parts("Abbasov, Ruslan")
    assert surname == "Abbasov"
    assert given == "Ruslan"

    # With extra whitespace
    surname, given = extract_name_parts("  Kerimov ,  Emil  ")
    assert surname == "Kerimov"
    assert given == "Emil"

    # Name without comma
    surname, given = extract_name_parts("JohnDoe")
    assert surname == "Unknown"
    assert given == "JohnDoe"

    # Unknown placeholders
    surname, given = extract_name_parts("___, ___")
    assert surname == "___"
    assert given == "___"


def test_surname_path_helpers():
    file_path = get_surname_file_path("Abbasov")
    rel_path = get_surname_relative_path("Abbasov")
    assert file_path.replace("\\", "/").endswith("surnames/abbasov.html")
    assert rel_path == "surnames/abbasov.html"

    # Special characters and spaces
    special_file = get_surname_file_path("O'Connor-Smith Jr.")
    special_rel = get_surname_relative_path("O'Connor-Smith Jr.")
    assert special_rel == "surnames/oconnorsmith_jr.html"
    assert special_file.replace("\\", "/").endswith("surnames/oconnorsmith_jr.html")

    # Underscores (placeholder surname)
    placeholder_file = get_surname_file_path("___")
    placeholder_rel = get_surname_relative_path("___")
    assert placeholder_rel == "surnames/___.html"
    assert placeholder_file.replace("\\", "/").endswith("surnames/___.html")


def test_individual_path_helpers():
    file_path = get_individual_file_path("Abbasov", "Ruslan", "ee478feff4648214c729833c19e8dc")
    rel_path = get_individual_relative_path("Abbasov", "Ruslan", "ee478feff4648214c729833c19e8dc")

    assert file_path.replace("\\", "/").endswith("ppl/abbasov/ruslan_ee478fef.html")
    assert rel_path == "ppl/abbasov/ruslan_ee478fef.html"

    # Special characters in names
    special_file = get_individual_file_path("O'Neill", "Mary-Jane", "1234567890abcdef1234567890abcd")
    special_rel = get_individual_relative_path("O'Neill", "Mary-Jane", "1234567890abcdef1234567890abcd")

    assert special_rel == "ppl/oneill/maryjane_12345678.html"
    assert special_file.replace("\\", "/").endswith("ppl/oneill/maryjane_12345678.html")
