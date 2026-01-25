# frederick_sports
Sandbox for Frederick News-Post experiments

## High School Hangout Standings

Interactive HTML standings tables for Frederick County high school sports, extracted from The Frederick News-Post High School Hangout PDF.

**View the published site:** https://newsappsUMD.github.io/frederick_sports/

### Available Sports

- Football
- Girls Flag Football
- Boys Soccer
- Girls Soccer
- Volleyball
- Field Hockey
- Cross Country
- Golf

## Usage

### Parsing PDFs

To extract data from High School Hangout PDFs and generate HTML pages:

1. Place the PDF file in the `hs_hangout/` directory with the naming format `YYYY_MM_DD.pdf` (e.g., `2025_12_06.pdf`)

2. Run the parser:
```bash
python process_pdfs.py
```

This will:
- Extract statistics and standings from all sports in the PDF
- Generate JSON data files in `data/YYYY_MM_DD/`
- Create HTML pages in `docs/` for GitHub Pages

### Output Files

For each sport and date, the following files are generated:

**Data files** (in `data/YYYY_MM_DD/`):
- `{sport}_data.json` - Player statistics
- `{sport}_standings.json` - Team standings
- `{sport}.html` - Full HTML page

**Published files** (in `docs/`):
- `{sport}_YYYY_MM_DD.html` - Main page
- `player_stats_{sport}_YYYY_MM_DD.html` - Player statistics page
- `standings_{sport}_YYYY_MM_DD.html` - Standings page

### Publishing to GitHub Pages

The site is automatically published from the `docs/` directory via GitHub Pages.

To publish updates:

1. Parse the latest PDF (see above)
2. Commit the changes:
```bash
git add data/ docs/
git commit -m "Update stats for [date]"
git push
```

3. The site will automatically update at https://newsappsUMD.github.io/frederick_sports/

### Structure

- `hs_hangout/` - Source PDF files
- `data/` - Extracted JSON data organized by date
- `docs/` - Published HTML files for GitHub Pages
- `extract_pdf.py` - PDF parsing and HTML generation functions
- `process_pdfs.py` - Main processing script
