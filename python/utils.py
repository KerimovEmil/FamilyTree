#!/usr/bin/env python3
"""
Utility functions for generating HTML files from GEDCOM data.
"""

import os
import hashlib
import re
from constants import OUTPUT_DIR, SURNAMES_DIR

def generate_id_from_pointer(pointer):
    """Generate a unique ID from a GEDCOM pointer."""
    # Remove the @ symbols and create a hash
    clean_pointer = pointer.replace('@', '')
    # Create a hash to ensure unique IDs
    hash_obj = hashlib.md5(clean_pointer.encode())
    return hash_obj.hexdigest()[:30]

def get_file_path(individual_id):
    """Generate the file path for an individual based on their ID."""
    # Use the first two characters of the ID for the directory structure
    dir1 = individual_id[0]
    dir2 = individual_id[1]
    filename = f"{individual_id}.html"
    return os.path.join(OUTPUT_DIR, dir1, dir2, filename)

def get_relative_path(individual_id):
    """Generate the relative path for an individual based on their ID."""
    dir1 = individual_id[0]
    dir2 = individual_id[1]
    filename = f"{individual_id}.html"
    return f"ppl/{dir1}/{dir2}/{filename}"

def get_surname_file_path(surname):
    """Generate the file path for a surname page."""
    # Convert surname to a safe filename by replacing spaces with underscores
    # and removing any special characters
    safe_surname = re.sub(r'[^\w\s]', '', surname).lower().replace(' ', '_')
    return os.path.join(SURNAMES_DIR, f"{safe_surname}.html")

def get_surname_relative_path(surname):
    """Generate the relative path for a surname page."""
    # Convert surname to a safe filename by replacing spaces with underscores
    # and removing any special characters
    safe_surname = re.sub(r'[^\w\s]', '', surname).lower().replace(' ', '_')
    return f"{SURNAMES_DIR}/{safe_surname}.html"

def get_individual_file_path(surname, given_name, individual_id):
    """Generate the file path for an individual based on surname and given name."""
    # Convert surname and given name to safe filenames
    safe_surname = re.sub(r'[^\w\s]', '', surname).lower().replace(' ', '_')
    safe_given_name = re.sub(r'[^\w\s]', '', given_name).lower().replace(' ', '_')

    # Create a unique filename using the individual_id as a suffix to handle duplicates
    filename = f"{safe_given_name}_{individual_id[:8]}.html"

    # Create the directory path
    dir_path = os.path.join(OUTPUT_DIR, safe_surname)

    return os.path.join(dir_path, filename)

def get_individual_relative_path(surname, given_name, individual_id):
    """Generate the relative path for an individual based on surname and given name."""
    # Convert surname and given name to safe filenames
    safe_surname = re.sub(r'[^\w\s]', '', surname).lower().replace(' ', '_')
    safe_given_name = re.sub(r'[^\w\s]', '', given_name).lower().replace(' ', '_')

    # Create a unique filename using the individual_id as a suffix to handle duplicates
    filename = f"{safe_given_name}_{individual_id[:8]}.html"

    # Return the path relative to the root directory
    return f"{OUTPUT_DIR}/{safe_surname}/{filename}"
