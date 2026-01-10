#!/usr/bin/env python3
"""
Standings Validation Script

This script validates parsed standings JSON against the original PDF text.
It extracts raw standings data from the PDF and compares it to the parsed output,
reporting any discrepancies.

Usage:
    python validate_standings.py [--date YYYY_MM_DD] [--sport SPORT]

    If no date is specified, validates all dates.
    If no sport is specified, validates all sports with standings.
"""

import argparse
import json
import os
from typing import Dict, List, Tuple

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install PyMuPDF")
    exit(1)


def extract_pdf_text(pdf_path: str) -> str:
    """Extract all text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def find_cmc_section(text: str, section_index: int) -> Tuple[str, int, int]:
    """
    Find a specific CENTRAL MARYLAND CONFERENCE section in the PDF text.

    Returns the section text, start line, and end line.
    """
    lines = text.split('\n')

    # Find all CMC section starts
    cmc_starts = []
    for i, line in enumerate(lines):
        if 'CENTRAL MARYLAND CONFERENCE' in line:
            cmc_starts.append(i)

    if section_index >= len(cmc_starts):
        return "", -1, -1

    start = cmc_starts[section_index]

    # Find the end of this section
    end = len(lines)
    stop_markers = ['INDIVIDUAL LEADERS', 'FCPS', 'OTHER SCHOOLS', 'PASSING',
                    'RUSHING', 'SCORING LEADERS', 'GOALKEEPER']

    for i in range(start + 1, len(lines)):
        line_upper = lines[i].upper().strip()
        if any(marker in line_upper for marker in stop_markers):
            end = i
            break

    section_text = '\n'.join(lines[start:end])
    return section_text, start, end


def extract_raw_standings_from_section(section_text: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Extract raw standings data from a CMC section text.
    Returns a dict of division -> list of team records.
    """
    standings = {}
    lines = section_text.split('\n')

    # Flatten all values
    values = []
    for line in lines:
        parts = [p.strip() for p in line.split('\t') if p.strip()]
        values.extend(parts)

    # Remove header words
    header_words = {'Team', 'W', 'L', 'T', 'Division', 'Overall', 'CENTRAL', 'MARYLAND', 'CONFERENCE'}
    values = [v for v in values if v not in header_words]

    current_division = None
    idx = 0

    while idx < len(values):
        val = values[idx]

        # Check for division headers
        if 'DIVISION' in val or 'SCHOOL' in val:
            current_division = val.strip()
            standings[current_division] = []
            idx += 1
            continue

        # Check if this is a team name
        if current_division is not None and not val.replace('.', '').replace(',', '').isdigit():
            team_name = val

            # Collect numeric values
            stats = []
            j = idx + 1
            while j < len(values) and len(stats) < 6:
                next_val = values[j]
                if 'DIVISION' in next_val or 'SCHOOL' in next_val:
                    break
                if not next_val.replace('.', '').replace(',', '').isdigit():
                    break
                if next_val.replace(',', '').isdigit():
                    stats.append(next_val)
                j += 1

            if stats:
                standings[current_division].append({
                    'team': team_name,
                    'raw_stats': stats,
                    'num_values': len(stats)
                })

            idx = j
            continue

        idx += 1

    return standings


def validate_standings(pdf_path: str, json_path: str, section_index: int, sport_name: str) -> List[str]:
    """
    Validate parsed standings against PDF text.

    Returns a list of validation messages (empty if all valid).
    """
    messages = []

    if not os.path.exists(pdf_path):
        return [f"PDF not found: {pdf_path}"]

    if not os.path.exists(json_path):
        return [f"JSON not found: {json_path}"]

    # Extract PDF text and find the relevant section
    pdf_text = extract_pdf_text(pdf_path)
    section_text, start_line, end_line = find_cmc_section(pdf_text, section_index)

    if not section_text:
        return [f"CMC section {section_index} not found in PDF"]

    # Extract raw standings from section
    raw_standings = extract_raw_standings_from_section(section_text)

    # Load parsed JSON
    with open(json_path, 'r') as f:
        parsed_standings = json.load(f)

    # Compare divisions
    raw_divisions = set(raw_standings.keys())
    parsed_divisions = set(parsed_standings.keys())

    if raw_divisions != parsed_divisions:
        messages.append(f"Division mismatch!")
        messages.append(f"  Raw: {sorted(raw_divisions)}")
        messages.append(f"  Parsed: {sorted(parsed_divisions)}")

    # Compare teams in each division
    for division in raw_divisions.intersection(parsed_divisions):
        # Compare team counts
        if len(raw_standings[division]) != len(parsed_standings[division]):
            messages.append(f"{division}: Team count mismatch")
            messages.append(f"  Raw: {len(raw_standings[division])} teams")
            messages.append(f"  Parsed: {len(parsed_standings[division])} teams")

        # Validate numeric values
        for i, raw_team in enumerate(raw_standings[division]):
            if i >= len(parsed_standings[division]):
                messages.append(f"{division}: Missing team {raw_team['team']} in parsed output")
                continue

            parsed_team = parsed_standings[division][i]
            raw_stats = raw_team['raw_stats']

            # Build expected values from parsed team
            parsed_values = []
            if raw_team['num_values'] == 6:
                # 6-value format (with ties)
                parsed_values = [
                    parsed_team.get('div_wins', ''),
                    parsed_team.get('div_losses', ''),
                    parsed_team.get('div_ties', ''),
                    parsed_team.get('overall_wins', ''),
                    parsed_team.get('overall_losses', ''),
                    parsed_team.get('overall_ties', '')
                ]
            elif raw_team['num_values'] == 4:
                # 4-value format (no ties)
                parsed_values = [
                    parsed_team.get('div_wins', ''),
                    parsed_team.get('div_losses', ''),
                    parsed_team.get('overall_wins', ''),
                    parsed_team.get('overall_losses', '')
                ]

            # Compare values
            if len(raw_stats) == len(parsed_values):
                for j, (raw_val, parsed_val) in enumerate(zip(raw_stats, parsed_values)):
                    if raw_val != parsed_val:
                        messages.append(f"{division} - {raw_team['team']}: Value mismatch at position {j}")
                        messages.append(f"  Raw: {raw_val}, Parsed: {parsed_val}")

    return messages


def print_raw_section(pdf_path: str, section_index: int, sport_name: str):
    """Print the raw PDF section for debugging."""
    pdf_text = extract_pdf_text(pdf_path)
    section_text, start, end = find_cmc_section(pdf_text, section_index)

    print(f"\n{'='*80}")
    print(f"RAW PDF SECTION: {sport_name} (CMC index {section_index})")
    print(f"Lines {start} to {end}")
    print('='*80)

    if section_text:
        # Show first 50 lines of the section
        lines = section_text.split('\n')[:50]
        for i, line in enumerate(lines):
            # Show tabs explicitly
            display_line = line.replace('\t', '[TAB]')
            print(f"{start + i:4d}: {display_line}")
        all_lines = section_text.split('\n')
        if len(all_lines) > 50:
            print(f"... ({len(all_lines) - 50} more lines)")
    else:
        print("Section not found!")

    # Also show extracted raw standings
    raw_standings = extract_raw_standings_from_section(section_text)
    print(f"\n{'='*80}")
    print("EXTRACTED RAW STANDINGS:")
    print('='*80)
    for division, teams in raw_standings.items():
        print(f"\n{division}:")
        for team in teams:
            print(f"  {team['team']}: {team['raw_stats']} ({team['num_values']} values)")


def main():
    parser = argparse.ArgumentParser(description='Validate standings against PDF')
    parser.add_argument('--date', type=str, help='Date folder (YYYY_MM_DD)')
    parser.add_argument('--sport', type=str, help='Sport to validate')
    parser.add_argument('--show-raw', action='store_true', help='Show raw PDF sections')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()

    # Configuration for CMC standings
    cmc_config = {
        '2025_10_23': {
            'boys_soccer': 2,
            'girls_soccer': 3,
            'volleyball': 0,
            'field_hockey': 1,
        },
        '2025_12_06': {
            'boys_soccer': 1,
            'girls_soccer': 3,
            'volleyball': 2,
            'field_hockey': 0,
        }
    }

    # Determine which dates to validate
    dates = [args.date] if args.date else list(cmc_config.keys())

    all_valid = True

    for date in dates:
        if date not in cmc_config:
            print(f"Warning: No config for date {date}")
            continue

        pdf_path = f"hs_hangout/{date}.pdf"

        print(f"\n{'#'*80}")
        print(f"# VALIDATING: {date}")
        print('#'*80)

        # Determine which sports to validate
        sports = [args.sport] if args.sport else list(cmc_config[date].keys())

        for sport in sports:
            if sport not in cmc_config[date]:
                print(f"Warning: {sport} not configured for {date}")
                continue

            section_index = cmc_config[date][sport]
            json_path = f"data/{date}/{sport}_standings.json"

            print(f"\n{'='*60}")
            print(f"Validating {sport} (CMC section {section_index})")
            print('='*60)

            if args.show_raw:
                print_raw_section(pdf_path, section_index, sport)

            messages = validate_standings(pdf_path, json_path, section_index, sport)

            if messages:
                all_valid = False
                print(f"\nVALIDATION ISSUES:")
                for msg in messages:
                    print(f"  {msg}")
            else:
                print(f"\nVALIDATION PASSED")

            # Show parsed vs expected comparison
            if args.verbose:
                if os.path.exists(json_path):
                    with open(json_path, 'r') as f:
                        parsed = json.load(f)
                    print(f"\nParsed standings:")
                    for div, teams in parsed.items():
                        print(f"\n  {div}:")
                        for team in teams:
                            div_record = f"{team.get('div_wins', '?')}-{team.get('div_losses', '?')}-{team.get('div_ties', '?')}"
                            ovr_record = f"{team.get('overall_wins', '?')}-{team.get('overall_losses', '?')}-{team.get('overall_ties', '?')}"
                            print(f"    {team['team']}: Div {div_record}, Ovr {ovr_record}")

    print(f"\n{'#'*80}")
    if all_valid:
        print("# ALL VALIDATIONS PASSED")
    else:
        print("# SOME VALIDATIONS FAILED - SEE ABOVE FOR DETAILS")
    print('#'*80)

    return 0 if all_valid else 1


if __name__ == '__main__':
    exit(main())
