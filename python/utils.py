#!/usr/bin/env python3
"""
Utility functions for generating HTML files from GEDCOM data.
"""

import os
import hashlib
from constants import OUTPUT_DIR

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
