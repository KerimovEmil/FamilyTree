# FamilyTree Improvement Plan (TODOs)

This document tracks the planned bug fixes, refactorings, and feature enhancements for the FamilyTree static site generator. Each numbered item is scoped to be completed in its own standalone Pull Request.

---

## Phase 1: Bug Fixes & HTML Validity

### [x] TODO 1: Standardize Relative Links & Remove Hardcoded `../../../FamilyTree/` Paths
- **Problem**: Links inside individual pages (`ppl/<surname>/<person>.html`) and templates in `python/constants.py` and `python/html_generation.py` use `../../../FamilyTree/{path}` instead of `../../{path}`. This breaks navigation when serving the site locally (e.g., `python -m http.server`) or under a custom domain.
- **Scope**:
  - Replace all `../../../FamilyTree/` prefixes in `python/constants.py` and `python/html_generation.py` with `../../`.
  - Regenerate static HTML pages and verify all internal navigation links work both locally and on GitHub Pages.

### [x] TODO 2: Fix Malformed HTML Table Tags in Templates
- **Problem**: `PARENT_ROW_TEMPLATE`, `FAMILY_ROW_TEMPLATE`, and `CHILD_ROW_TEMPLATE` in `python/constants.py` contain invalid self-closing `<td />` tags (e.g., `<td class="ColumnValue" /><a href=...>`). Also, `HTML_TEMPLATE` has an unclosed/nested `<tr>` inside the Events table.
- **Scope**:
  - Fix all `<td />` occurrences in `python/constants.py` to properly wrap cell contents with `<td>...</td>`.
  - Fix nested `<tr>` structure in `HTML_TEMPLATE`.
  - Regenerate static HTML pages.

### [x] TODO 3: Fix Surname Filename Sanitization Consistency
- **Problem**: `utils.get_surname_file_path()` and `utils.get_surname_relative_path()` strip special characters (`re.sub(r'[^\w\s]', '', surname)`), but `generate_index_html()` and `generate_surname_pages()` in `python/html_generation.py` bypass these helpers and only run `surname.lower().replace(' ', '_')`.
- **Scope**:
  - Update `generate_index_html()` and `generate_surname_pages()` to use `get_surname_file_path()` and `get_surname_relative_path()` from `python/utils.py`.
  - Ensure consistent handling of unknown/empty surnames (`"Unknown"`, `"___"`).
  - Regenerate static HTML pages.

### [ ] TODO 4: Support Single-Parent Families in Family & Pedigree Sections
- **Problem**: `generate_families_section()` and `generate_pedigree_section()` in `python/html_generation.py` skip an entire family (`if not spouse: continue`) when a spouse is unrecorded, hiding any children belonging to that family.
- **Scope**:
  - Update `generate_families_section()` and `generate_pedigree_section()` to render families and their children even when the spouse is missing/unknown.
  - Regenerate static HTML pages.

---

## Phase 2: Data Completeness & Escaping

### [ ] TODO 5: Display Death Events, Places, and Attributes on Individual Pages
- **Problem**: `HTML_TEMPLATE` only renders a hardcoded `Birth` date row and ignores `death_date`, birth/death places, occupation, and attributes (`get_occupation()` and `get_attributes()` exist in `python/data_extraction.py` but are never wired up).
- **Scope**:
  - Extract birth place and death place in `python/data_extraction.py`.
  - Render Death event row (when present) and event places/descriptions in the Events section.
  - Wire up occupation and attributes sections on individual pages when data is present.
  - Regenerate static HTML pages.

### [ ] TODO 6: Add HTML Escaping for GEDCOM Data Fields
- **Problem**: Strings parsed from GEDCOM (names, dates, places, notes) are interpolated directly into HTML templates via `.format()`, which can break HTML rendering if values contain `<`, `>`, `&`, or quotes.
- **Scope**:
  - Apply `html.escape()` to extracted text values before rendering into HTML templates.
  - Regenerate static HTML pages.

---

## Phase 3: Code Refactoring & Cleanup

### [ ] TODO 7: Refactor `generate_ancestors_section` to Use a Data-Driven / Recursive Approach
- **Problem**: `generate_ancestors_section()` in `python/html_generation.py` is over 320 lines of repetitive, copy-pasted code for each individual ancestor slot across 4 generations.
- **Scope**:
  - Replace the hardcoded ancestor blocks with a concise recursive or table-driven layout generator that produces identical HTML/CSS output.
  - Verify no visual regressions in the generated ancestor trees.

### [ ] TODO 8: Remove Dead and Duplicate Code Across Python Modules
- **Problem**:
  - `extract_name_parts()` is duplicated in `python/main.py` and `python/html_generation.py`.
  - `create_safe_filename()` in `python/main.py` is unused.
  - `get_file_path()`, `get_relative_path()` in `python/utils.py` and the fallback in `get_path_for_individual()` reference an obsolete `ppl/a/b/` directory structure.
  - `PEDIGREE_TEMPLATE` is defined twice in `python/constants.py`.
- **Scope**:
  - Consolidate shared helpers into `python/utils.py`.
  - Remove unused functions and duplicate constants.

---

## Phase 4: Features, Testing & Automation

### [ ] TODO 9: Add Unit & Integration Tests
- **Problem**: There are currently no automated tests verifying GEDCOM parsing, path sanitization, or HTML generation.
- **Scope**:
  - Add a `tests/` suite using `pytest` or `unittest`.
  - Test name extraction, filename sanitization, single-parent families, and end-to-end HTML generation on a sample GEDCOM fixture.

### [ ] TODO 10: Add Client-Side Search/Filter to Index and Individuals Pages
- **Problem**: Navigating large lists of surnames (`index.html`) and individuals (`individuals.html`) requires manual scrolling or browser find.
- **Scope**:
  - Add a lightweight search/filter input box to `index.html` and `individuals.html` to filter table rows in real time.

### [ ] TODO 11: Add GitHub Actions Workflow for Automated Build & GitHub Pages Deployment
- **Problem**: Every GEDCOM update requires manually running `python generate_html_from_gedcom.py` locally and committing hundreds of generated HTML files.
- **Scope**:
  - Add a `.github/workflows/` CI/CD workflow that runs the Python generator on push to `main`, runs tests, and automatically deploys the generated site to GitHub Pages.
