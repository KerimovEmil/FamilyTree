#!/usr/bin/env python3
"""
Main script to generate HTML files from a GEDCOM file.
The HTML files will be saved in the ppl directory with a specific structure.
"""

import os
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser

from constants import GEDCOM_FILE
from utils import generate_id_from_pointer, get_file_path
from data_extraction import get_name, get_birth_data, get_death_data
from html_generation import (
    generate_html_for_individual, generate_index_html, generate_individuals_html
)

def main():
    """Main function to parse GEDCOM and generate HTML files."""
    # Parse the GEDCOM file
    gedcom_parser = Parser()
    gedcom_parser.parse_file(GEDCOM_FILE)

    # Dictionary to store individual data
    individuals_data = {}

    # Process each individual
    for element in gedcom_parser.get_root_child_elements():
        if isinstance(element, IndividualElement):
            # Generate HTML content
            html_content = generate_html_for_individual(gedcom_parser, element)

            # Determine file path
            individual_id = generate_id_from_pointer(element.get_pointer())
            file_path = get_file_path(individual_id)

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write HTML file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Store individual data for index and individuals pages
            name = get_name(element)
            birth_date, _ = get_birth_data(element)
            death_date, _ = get_death_data(element)

            individuals_data[individual_id] = {
                'name': name,
                'birth_date': birth_date,
                'death_date': death_date
            }

            print(f"Generated HTML file for {name} at {file_path}")

    # Generate index.html and individuals.html
    generate_index_html(individuals_data)
    generate_individuals_html(individuals_data)

if __name__ == "__main__":
    main()
