#!/usr/bin/env python3
"""
Process all sports from both PDFs.
This script properly parses each PDF independently for all sports.
"""

import sys
import os
import shutil
from pathlib import Path

# Set the PDF path before importing extract_pdf
def process_pdf_for_all_sports(pdf_path, date_str):
    """Process a single PDF for all sports."""

    print(f"\n{'='*80}")
    print(f"PROCESSING ALL SPORTS FROM: {pdf_path}")
    print(f"Date: {date_str}")
    print(f"{'='*80}\n")

    # Temporarily modify extract_pdf.py to use this PDF
    original_extract_pdf = Path('extract_pdf.py').read_text()

    # Replace the PDF path in extract_pdf.py
    modified_extract_pdf = original_extract_pdf.replace(
        "pdf_path = 'hs_hangout/2025_12_06.pdf'",
        f"pdf_path = '{pdf_path}'"
    )

    # Also need to update the date in file outputs
    if '10_23' in date_str:
        modified_extract_pdf = modified_extract_pdf.replace('2025_12_06', '2025_10_23')

    # Write modified version
    Path('extract_pdf_temp.py').write_text(modified_extract_pdf)

    # Run the extraction
    import subprocess
    result = subprocess.run(
        ['python3', 'extract_pdf_temp.py'],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    # Cleanup
    Path('extract_pdf_temp.py').unlink()

    # Move generated files to data folder
    output_dir = Path('data') / date_str
    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy JSON files
    for json_file in Path('.').glob('*_stats.json'):
        if json_file.name not in ['extract_pdf.py', 'process_all_pdfs.py', 'process_all_sports.py']:
            dest = output_dir / json_file.name
            shutil.copy(json_file, dest)
            print(f"  → Saved {json_file.name} to {dest}")

    print(f"\n{'='*80}")
    print(f"COMPLETED: {date_str}")
    print(f"{'='*80}\n")


def main():
    """Process both PDFs."""

    # Process October 2025
    process_pdf_for_all_sports(
        pdf_path='hs_hangout/2025_10_23.pdf',
        date_str='2025_10_23'
    )

    # Process December 2025
    process_pdf_for_all_sports(
        pdf_path='hs_hangout/2025_12_06.pdf',
        date_str='2025_12_06'
    )

    print("\n" + "="*80)
    print("✓ ALL SPORTS PROCESSED FOR BOTH DATES!")
    print("="*80)
    print("\nGenerated files:")
    print("  - docs/ folder: HTML pages for GitHub Pages")
    print("  - hs_hangout/ folder: HTML pages (source)")
    print("  - data/ folders: JSON data files")


if __name__ == '__main__':
    main()
