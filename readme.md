# Family Tree Website Generator

A Python-based tool that generates a static HTML website from GEDCOM genealogy files. This project creates a browsable family tree website with individual pages organized by surname, an index page, and surname-specific pages.

## Features

- Generates individual HTML pages for each person in the family tree
- Organizes pages by surname for easy navigation
- Creates index and surname summary pages
- Displays birth and death information
- Shows family relationships including parents, siblings, spouses, and children
- Generates pedigree and ancestor tree visualizations

## Project Structure

```
├── css/                  # Stylesheet files for the HTML pages
├── ged/                  # Directory for GEDCOM files
│   └── family_tree.ged   # Your family tree GEDCOM file
├── images/               # Images used in the website
├── ppl/                  # Generated individual HTML pages organized by surname
├── python/               # Python modules for HTML generation
├── surnames/             # Generated surname-specific HTML pages
├── generate_html_from_gedcom.py  # Main script to run
├── index.html            # Generated main index page
├── individuals.html      # Generated list of all individuals
└── requirements.txt      # Python dependencies
```

## Setup

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Generating the Website

1. Place your GEDCOM file in the `ged` directory as `family_tree.ged`
2. Run the generation script:

```bash
python generate_html_from_gedcom.py
```

3. The script will generate HTML files in the `ppl` directory organized by surname
4. Open `index.html` in your web browser to view the family tree

### Customization

You can customize the HTML templates by modifying the template strings in `python/constants.py`.

## Troubleshooting

- If you encounter issues with GEDCOM parsing, ensure your GEDCOM file follows the standard format
- For large family trees, the generation process may take several minutes

## License

This project is licensed under the MIT License - see the LICENSE file for details.
