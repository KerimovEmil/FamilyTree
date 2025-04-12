#!/usr/bin/env python3
"""
Script to generate HTML files from a GEDCOM file with a new directory structure.
The HTML files will be saved in the ppl directory organized by surname.
"""

import os
import sys

# Add the python directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))

# Import the main function from the main module
from main import main

if __name__ == "__main__":
    # Clean up old directories if they exist
    if os.path.exists('ppl'):
        print("Cleaning up old ppl directory...")
        import shutil
        shutil.rmtree('ppl')

    if os.path.exists('surnames'):
        print("Cleaning up old surnames directory...")
        import shutil
        shutil.rmtree('surnames')

    # Run the main function to generate HTML files
    print("Generating HTML files with new structure...")
    main()

    print("\nGeneration completed.")
    print("Individual pages are now organized by surname in the 'ppl' directory.")
    print("Surname pages are in the 'surnames' directory.")
