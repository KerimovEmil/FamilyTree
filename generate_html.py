#!/usr/bin/env python3
"""
Wrapper script to run the HTML generation from the root directory.
"""

import os
import sys

# Add the python directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))

# Import and run the main function
from python.main import main

if __name__ == "__main__":
    main()
