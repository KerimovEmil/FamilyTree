#!/usr/bin/env python3
"""
Main script to generate HTML files from a GEDCOM file with a new directory structure.
The HTML files will be saved in the ppl directory organized by surname.
"""

import os
import re
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser

from constants import GEDCOM_FILE
from utils import (
    generate_id_from_pointer, get_individual_file_path, get_individual_relative_path
)
from data_extraction import get_name, get_birth_data, get_death_data
from html_generation import (
    generate_html_for_individual, generate_index_html, generate_individuals_html, generate_surname_pages
)

def extract_name_parts(name):
    """Extract surname and given name from a full name."""
    if ',' in name:
        surname, given_name = name.split(',', 1)
        return surname.strip(), given_name.strip()
    else:
        # Handle cases where there's no comma in the name
        return "Unknown", name

def create_safe_filename(text):
    """Create a safe filename from text."""
    # Replace spaces with underscores and remove special characters
    return re.sub(r'[^\w\s]', '', text).lower().replace(' ', '_')

def main():
    """Main function to parse GEDCOM and generate HTML files with new structure."""
    # Parse the GEDCOM file
    gedcom_parser = Parser()
    gedcom_parser.parse_file(GEDCOM_FILE)

    # Dictionary to store individual data
    individuals_data = {}

    # First pass: collect all individual data
    for element in gedcom_parser.get_root_child_elements():
        if isinstance(element, IndividualElement):
            # Get individual details
            individual_id = generate_id_from_pointer(element.get_pointer())
            name = get_name(element)
            surname, given_name = extract_name_parts(name)
            birth_date = get_birth_data(element)
            death_date = get_death_data(element)

            # Determine file path using the new structure
            file_path = get_individual_file_path(surname, given_name, individual_id)
            relative_path = get_individual_relative_path(surname, given_name, individual_id)

            # Store individual data
            individuals_data[individual_id] = {
                'name': name,
                'birth_date': birth_date,
                'death_date': death_date,
                'surname': surname,
                'given_name': given_name,
                'path': relative_path,
                'element': element
            }

    # Second pass: generate HTML files with all paths available
    for individual_id, data in individuals_data.items():
        # Generate HTML content
        html_content = generate_html_for_individual(gedcom_parser, data['element'], individuals_data)

        # Get the file path
        file_path = get_individual_file_path(data['surname'], data['given_name'], individual_id)

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write HTML file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Generated HTML file for {data['name']} at {file_path}")

    # Generate index.html, individuals.html, and surname pages with updated paths
    generate_index_html(individuals_data)
    generate_individuals_html(individuals_data)
    generate_surname_pages(individuals_data)

    print("HTML generation completed with new directory structure.")

if __name__ == "__main__":
    main()
