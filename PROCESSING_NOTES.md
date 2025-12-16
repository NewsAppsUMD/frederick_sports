# PDF Processing Notes

## Repository Organization

The repository is now organized with each PDF having its own folder:

```
data/
├── 2025_10_23/
│   ├── 2025_10_23.pdf (copy of source PDF)
│   ├── full_text.txt (extracted PDF text)
│   └── football.html (generated HTML with standings + stats)
├── 2025_12_06/
│   ├── 2025_12_06.pdf (copy of source PDF)
│   ├── full_text.txt (extracted PDF text)
│   └── football.html (generated HTML with standings + stats)
```

## How to Process PDFs

### Automated Processing

Run the `process_all_pdfs.py` script to process all PDFs:

```bash
python3 process_all_pdfs.py
```

This script:
1. Extracts text from each PDF
2. Parses football statistics (rushing, passing, receiving)
3. Combines with team standings
4. Generates complete HTML pages
5. Saves to both `data/` and `docs/` folders

### Important: Section Indices

Different PDF editions have sports in different order. The script uses specific section indices:

**October 2025 (2025_10_23.pdf):**
- Section 0: Volleyball
- Section 1: Girls Flag Football
- Section 2: **Football (Boys)** ← Used for football parsing

**December 2025 (2025_12_06.pdf):**
- Section 0: Girls Flag Football
- Section 1: **Football (Boys)** ← Used for football parsing
- Section 2: Volleyball

## Data Verification

The script correctly parses different stats for each date:

**October 2025:**
- Bradly Matthews: 140 Att, 1,256 Yds (mid-season)

**December 2025:**
- Bradly Matthews: 246 Att, 2,124 Yds (end of season)

## Files Generated

For each date, the following files are created:

- `data/{date}/football.html` - Complete page with standings and player stats
- `docs/football_{date}.html` - Copy for GitHub Pages deployment

## Adding New PDFs

To add a new PDF:

1. Place the PDF in `hs_hangout/` folder with date format: `YYYY_MM_DD.pdf`
2. Update `process_all_pdfs.py` with the correct section index for football
3. Run the script to generate HTML pages

### Finding the Correct Section Index

Use this helper script to identify sections:

```python
with open('data/YYYY_MM_DD/full_text.txt', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'INDIVIDUAL LEADERS' in line:
        print(f"Section at line {i}:")
        for j in range(i, min(len(lines), i+5)):
            print(f"  {lines[j].rstrip()}")
```

Look for the section with "RUSHING" followed by player names like "Bradly Matthews" (boys football).

## Common Issues

### Issue: Wrong Sport Data Appears

**Cause:** Incorrect section index for the PDF
**Solution:** Find the correct section index using the helper script above

### Issue: No Data Parsed

**Cause:** PDF structure changed
**Solution:** Check the full_text.txt to see if the format changed

### Issue: Missing Players

**Cause:** PDF extraction issue or parsing logic needs adjustment
**Solution:** Review the raw PDF text extraction in full_text.txt
