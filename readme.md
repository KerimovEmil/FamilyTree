# My Family Tree

[![Deploy](https://github.com/KerimovEmil/FamilyTree/actions/workflows/deploy.yml/badge.svg)](https://github.com/KerimovEmil/FamilyTree/actions/workflows/deploy.yml)
[![Live Site](https://img.shields.io/badge/Live_Site-GitHub_Pages-2ea44f?style=flat&logo=github)](https://kerimovemil.github.io/FamilyTree/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, static site generator and interactive exploration platform for genealogy data. It converts a standard GEDCOM (`.ged`) file into an offline-capable, responsive family tree website featuring interactive graph projections, an intelligent relationship finder, adaptive pedigree trees, and individual profiles organized by surname.

🌐 **Explore the Live Site:** [https://kerimovemil.github.io/FamilyTree/](https://kerimovemil.github.io/FamilyTree/)

---

## Key Features

### 🌳 Native Interactive Family Tree (`interactive_graph.html`)
- **Self-Contained & Fast:** Uses a bundled [PeWu/topola](https://github.com/PeWu/topola) layout engine and D3.js zoom controller (`js/topola-bundle.min.js`), running 100% offline with zero third-party iframe dependencies.
- **4 View Projections:**
  - **Relatives:** Comprehensive all-in-one chart showing direct lineage and extended family.
  - **Hourglass:** Symmetrical tree displaying both direct ancestors and descendants of the focal person.
  - **Ancestors:** Direct maternal and paternal lineage tree.
  - **Descendants:** Direct progeny chart across generations.
- **Smart Focal Centering:** Automatically centers on Emil Kerimov (or URL query `?indi=<id>`) at a crisp, legible `0.9x` scale instead of shrinking to microscopic overview scale.
- **Fluid Pan & Zoom:** Natural scroll-wheel zoom, click-and-drag pan (`grabbing` cursor), `Fit View` for whole-tree overviews, and `🏠 Emil` quick home reset.
- **Autocomplete Search:** Responsive search bar with a clear (`×`) button to jump to any of the 355+ family members by name, birth/death year, or ID.
- **Interactive Action Popovers:** Clicking any card displays quick pathways to:
  - **View Profile &rarr;**: Opens their complete profile page (`ppl/...`).
  - **Center Tree Here**: Re-focuses the current tree projection on them.
  - **Find Relationship &rarr;**: Traces kinship to this person.
- **Double-Click Navigation:** Double-clicking any person node immediately re-centers the tree on that individual.

### 🔍 Interactive Relationship Finder (`relationship.html`)
- **Shortest-Path Graph Search:** Client-side Breadth-First Search (BFS) over bidirectional parent, child, and spouse edges to discover shortest connection paths between any two people.
- **Kinship Title Resolver:** Automatically calculates descriptive genealogical kinship titles (e.g., *"Maternal Grandmother"*, *"First Cousin Once Removed"*, *"Great-Uncle"*, *"Spouse"*).
- **Most Recent Common Ancestor (MRCA):** Identifies shared common ancestors for blood relatives and displays the genealogical generational distance.
- **Step-by-Step Connection Chain:** Renders an interactive visual card trail detailing each step in the relationship (e.g. `father → father → daughter → son`).
- **Shareable Deep Links:** Preserves selections in query parameters (`relationship.html?p1=<id>&p2=<id>`).

### 👤 Detailed Individual Profiles (`ppl/...`)
- **Surname Organization:** Individual pages are cleanly organized into surname subdirectories (e.g. `ppl/kerimov/emil_xxxx.html`).
- **Chronological Timeline:** Events ordered chronologically (Birth, Marriages, Occupations, Death).
- **Milestone Age Calculations:** Displays calculated ages at milestone events and age at death (e.g., *"Age 24"*, *"Age at Death: 74 years"*).
- **Cross-Navigation Links:** Every profile includes direct action links to view the person in the Interactive Graph (`?indi=<id>`) and find their relationship to others (`?p1=<id>`).

### 📑 Surname Indexes & Real-Time Filtering (`surnames/...`)
- Comprehensive surname directory and individual listings.
- Real-time client-side search filtering on surname pages with a clear button (`×`) and live match counter (e.g., *"Showing 12 of 34 individuals"*).

### 📐 Adaptive Pedigree Trees
- Symmetrical and asymmetrical ancestor tree layouts that dynamically adapt to missing parents/grandparents without misaligning branches.

---

## Project Structure

```
FamilyTree/
├── .github/
│   └── workflows/
│       └── deploy.yml            # CI/CD: lint, test, link crawl & GitHub Pages deploy
├── css/
│   ├── ancestortree.css          # Responsive pedigree tree layout styles
│   ├── behaviour.css             # Base behavior and typography
│   ├── interactive-graph.css     # Interactive graph toolbar, canvas & popover styles
│   ├── narrative-print.css       # Print layout stylesheet
│   └── narrative-screen.css      # Gramps narrative web report theme
├── ged/
│   └── family_tree.ged           # Single source of truth (GEDCOM file)
├── images/                       # Favicons and site assets
├── js/
│   ├── interactive_graph.js      # Client controller for the interactive graph viewer
│   ├── topola-bundle.min.js      # Minified standalone Topola + D3 zoom bundle (~178 KB)
│   └── README.md                 # Documentation on client JavaScript bundles
├── ppl/                          # Generated individual HTML pages by surname
├── python/
│   ├── constants.py              # HTML templates, CSS snippets & configuration
│   ├── data_extraction.py        # GEDCOM extraction (dates, ages, families, events)
│   ├── html_generation.py        # Generators for profiles, graph, and relationship pages
│   ├── main.py                   # Generation orchestration pipeline
│   └── utils.py                  # Sanitization, path generation & helpers
├── surnames/                     # Generated surname index & list pages
├── tests/
│   ├── fixtures/                 # Test GEDCOM snippets
│   ├── test_ancestor_layout.py   # Tests for pedigree tree branching
│   ├── test_data_extraction.py   # Tests for date parsing, ages, and attributes
│   ├── test_html_generation.py   # Tests for HTML generation and interactive views
│   └── test_utils.py             # Tests for name normalization and path helpers
├── tools/
│   └── check_links.py            # Headless crawler verifying link integrity
├── generate_html_from_gedcom.py  # Convenient entry point to regenerate the entire site
├── index.html                    # Generated main index / surname landing page
├── individuals.html              # Generated master individuals directory
├── interactive_graph.html        # Generated interactive tree viewer page
├── relationship.html             # Generated relationship finder page
└── requirements.txt              # Python dependencies (python-gedcom, pytest)
```

---

## Getting Started

### Prerequisites
- **Python 3.10+**
- **pip** (Python package installer)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/KerimovEmil/FamilyTree.git
   cd FamilyTree
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Generating the Website
`ged/family_tree.ged` is the single source of truth for the entire website. Any edits to this file will propagate automatically to all profiles, surname pages, and interactive views.

To generate or update all HTML files:
```bash
python generate_html_from_gedcom.py
```
*(Or alternatively: `python -m python.main`)*

### 2. Local Preview
Serve the generated site locally:
```bash
python -m http.server 8000
```
Open [http://localhost:8000](http://localhost:8000) in your web browser.

### 3. Running Automated Tests
Run the pytest test suite:
```bash
pytest tests/
```
All 21 unit and integration tests run in under 0.5s.

### 4. Link Integrity Crawl
To ensure all internal links between profiles, surnames, graphs, and relationship finders are healthy:
```bash
# Start the local server if not already running
python -m http.server 8000 &
# Run crawler across the site
python tools/check_links.py http://localhost:8000/individuals.html
python tools/check_links.py http://localhost:8000/interactive_graph.html
```
The script crawls all linked HTML pages and exits with code `0` if 0 broken links are found.

---

## Continuous Deployment

This repository uses **GitHub Actions** (`.github/workflows/deploy.yml`):
1. **Verification on Pull Requests:** Runs `pytest` and verifies link integrity via `tools/check_links.py`.
2. **Automated Deployment:** On push to `main`, regenerates the site, verifies links, and automatically deploys the static files to **GitHub Pages**.

---

## License

This project is open-source and licensed under the [MIT License](https://opensource.org/licenses/MIT).
