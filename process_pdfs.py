#!/usr/bin/env python3
"""
Comprehensive PDF processing script.
Processes ALL sports from each PDF and generates all HTML files.
"""

import sys
import json
from pathlib import Path

# Import all necessary functions from extract_pdf
from extract_pdf import (
    extract_text_from_pdf,
    # Parsing functions
    parse_football_stats,
    parse_soccer_stats,
    parse_volleyball_stats,
    parse_field_hockey_stats,
    parse_cross_country_stats,
    parse_golf_stats,
    parse_defensive_stats,
    # Structuring functions
    structure_stats,
    structure_soccer_stats,
    structure_volleyball_stats,
    structure_field_hockey_stats,
    structure_cross_country_stats,
    structure_golf_stats,
    # HTML generation functions
    generate_html,
    generate_soccer_html,
    generate_volleyball_html,
    generate_field_hockey_html,
    generate_cross_country_html,
    generate_golf_html,
)


def process_football_style_sport(text, sport_name, section_index, file_prefix, date_str, output_dir, docs_dir):
    """Process sports with rushing/passing/receiving stats (Football, Girls Flag Football)."""
    print(f"\n{'='*70}")
    print(f"Processing {sport_name}")
    print(f"{'='*70}")

    # Parse stats
    print(f"Parsing {sport_name} statistics...")
    stats_raw = parse_football_stats(text, section_index=section_index, sport_name=sport_name)

    # Structure the stats
    stats = structure_stats(stats_raw)

    print(f"{sport_name} stats parsed:")
    print(f"  Rushing leaders: {len(stats['rushing'])} entries")
    print(f"  Passing leaders: {len(stats['passing'])} entries")
    print(f"  Receiving leaders: {len(stats['receiving'])} entries")

    # Save JSON to data folder
    stats_file = output_dir / f'{file_prefix}_data.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"✓ Saved JSON to {stats_file}")

    # Load defensive stats if this is Girls Flag Football
    defensive_stats = None
    if sport_name == "Girls Flag Football":
        try:
            defensive_stats = parse_defensive_stats()
            print(f"  Defensive stats: {len(defensive_stats)} entries")
        except:
            print("  No defensive stats file found")

    # Generate HTML
    print(f"Generating HTML page...")
    html = generate_html(stats, sport_name, defensive_stats)

    # Save to data folder
    html_file = output_dir / f'{file_prefix}.html'
    with open(html_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved HTML to {html_file}")

    # Also save to docs folder for GitHub Pages
    docs_file = docs_dir / f'{file_prefix}_{date_str}.html'
    with open(docs_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved to docs: {docs_file}")

    # Also save player stats page
    player_stats_file = docs_dir / f'player_stats_{file_prefix}_{date_str}.html'
    with open(player_stats_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved player stats: {player_stats_file}")

    return stats


def process_soccer_sport(text, sport_name, file_prefix, date_str, output_dir, docs_dir):
    """Process soccer sports (Boys Soccer, Girls Soccer)."""
    print(f"\n{'='*70}")
    print(f"Processing {sport_name}")
    print(f"{'='*70}")

    # Parse stats
    print(f"Parsing {sport_name} statistics...")
    stats_raw = parse_soccer_stats(text, sport_name=sport_name)

    # Structure the stats
    stats = structure_soccer_stats(stats_raw)

    print(f"{sport_name} stats parsed:")
    print(f"  Scoring leaders: {len(stats['scoring'])} entries")
    print(f"  Goalkeepers: {len(stats['goalkeepers'])} entries")

    # Save JSON to data folder
    stats_file = output_dir / f'{file_prefix}_data.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"✓ Saved JSON to {stats_file}")

    # Generate HTML
    print(f"Generating HTML page...")
    html = generate_soccer_html(stats, sport_name)

    # Save to data folder
    html_file = output_dir / f'{file_prefix}.html'
    with open(html_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved HTML to {html_file}")

    # Also save to docs folder for GitHub Pages
    docs_file = docs_dir / f'{file_prefix}_{date_str}.html'
    with open(docs_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved to docs: {docs_file}")

    # Also save player stats and standings pages
    player_stats_file = docs_dir / f'player_stats_{file_prefix}_{date_str}.html'
    with open(player_stats_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved player stats: {player_stats_file}")

    standings_file = docs_dir / f'standings_{file_prefix}_{date_str}.html'
    with open(standings_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved standings: {standings_file}")

    return stats


def process_volleyball(text, date_str, output_dir, docs_dir):
    """Process volleyball stats."""
    sport_name = "Volleyball"
    file_prefix = "volleyball"

    print(f"\n{'='*70}")
    print(f"Processing {sport_name}")
    print(f"{'='*70}")

    # Parse stats
    print(f"Parsing {sport_name} statistics...")
    stats_raw = parse_volleyball_stats(text)

    # Structure the stats
    stats = structure_volleyball_stats(stats_raw)

    print(f"{sport_name} stats parsed:")
    print(f"  Kills leaders: {len(stats['kills'])} entries")
    print(f"  Assists leaders: {len(stats['assists'])} entries")
    print(f"  Digs leaders: {len(stats['digs'])} entries")

    # Save JSON to data folder
    stats_file = output_dir / f'{file_prefix}_data.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"✓ Saved JSON to {stats_file}")

    # Generate HTML
    print(f"Generating HTML page...")
    html = generate_volleyball_html(stats, sport_name)

    # Save to data folder
    html_file = output_dir / f'{file_prefix}.html'
    with open(html_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved HTML to {html_file}")

    # Also save to docs folder for GitHub Pages
    docs_file = docs_dir / f'{file_prefix}_{date_str}.html'
    with open(docs_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved to docs: {docs_file}")

    # Also save player stats and standings pages
    player_stats_file = docs_dir / f'player_stats_{file_prefix}_{date_str}.html'
    with open(player_stats_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved player stats: {player_stats_file}")

    standings_file = docs_dir / f'standings_{file_prefix}_{date_str}.html'
    with open(standings_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved standings: {standings_file}")

    return stats


def process_field_hockey(text, date_str, output_dir, docs_dir):
    """Process field hockey stats."""
    sport_name = "Field Hockey"
    file_prefix = "field_hockey"

    print(f"\n{'='*70}")
    print(f"Processing {sport_name}")
    print(f"{'='*70}")

    # Parse stats
    print(f"Parsing {sport_name} statistics...")
    stats_raw = parse_field_hockey_stats(text)

    # Structure the stats
    stats = structure_field_hockey_stats(stats_raw)

    print(f"{sport_name} stats parsed:")
    print(f"  Scoring leaders: {len(stats['scoring'])} entries")
    print(f"  Goalkeepers: {len(stats['goalkeepers'])} entries")

    # Save JSON to data folder
    stats_file = output_dir / f'{file_prefix}_data.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"✓ Saved JSON to {stats_file}")

    # Generate HTML
    print(f"Generating HTML page...")
    html = generate_field_hockey_html(stats, sport_name)

    # Save to data folder
    html_file = output_dir / f'{file_prefix}.html'
    with open(html_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved HTML to {html_file}")

    # Also save to docs folder for GitHub Pages
    docs_file = docs_dir / f'{file_prefix}_{date_str}.html'
    with open(docs_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved to docs: {docs_file}")

    # Also save player stats and standings pages
    player_stats_file = docs_dir / f'player_stats_{file_prefix}_{date_str}.html'
    with open(player_stats_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved player stats: {player_stats_file}")

    standings_file = docs_dir / f'standings_{file_prefix}_{date_str}.html'
    with open(standings_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved standings: {standings_file}")

    return stats


def process_cross_country(text, date_str, output_dir, docs_dir):
    """Process cross country stats."""
    sport_name = "Cross Country"
    file_prefix = "cross_country"

    print(f"\n{'='*70}")
    print(f"Processing {sport_name}")
    print(f"{'='*70}")

    # Parse stats
    print(f"Parsing {sport_name} statistics...")
    stats_raw = parse_cross_country_stats(text)

    # Structure the stats
    stats = structure_cross_country_stats(stats_raw)

    print(f"{sport_name} stats parsed:")
    print(f"  Boys top times: {len(stats['boys'])} entries")
    print(f"  Girls top times: {len(stats['girls'])} entries")

    # Save JSON to data folder
    stats_file = output_dir / f'{file_prefix}_data.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"✓ Saved JSON to {stats_file}")

    # Generate HTML
    print(f"Generating HTML page...")
    html = generate_cross_country_html(stats, sport_name)

    # Save to data folder
    html_file = output_dir / f'{file_prefix}.html'
    with open(html_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved HTML to {html_file}")

    # Also save to docs folder for GitHub Pages
    docs_file = docs_dir / f'{file_prefix}_{date_str}.html'
    with open(docs_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved to docs: {docs_file}")

    return stats


def process_golf(text, date_str, output_dir, docs_dir):
    """Process golf stats."""
    sport_name = "Golf"
    file_prefix = "golf"

    print(f"\n{'='*70}")
    print(f"Processing {sport_name}")
    print(f"{'='*70}")

    # Parse stats
    print(f"Parsing {sport_name} statistics...")
    stats_raw = parse_golf_stats(text)

    # Structure the stats
    stats = structure_golf_stats(stats_raw)

    print(f"{sport_name} stats parsed:")
    print(f"  Player leaders: {len(stats)} entries")

    # Save JSON to data folder
    stats_file = output_dir / f'{file_prefix}_data.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"✓ Saved JSON to {stats_file}")

    # Generate HTML
    print(f"Generating HTML page...")
    html = generate_golf_html(stats, sport_name)

    # Save to data folder
    html_file = output_dir / f'{file_prefix}.html'
    with open(html_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved HTML to {html_file}")

    # Also save to docs folder for GitHub Pages
    docs_file = docs_dir / f'{file_prefix}_{date_str}.html'
    with open(docs_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved to docs: {docs_file}")

    return stats


def process_pdf(pdf_path, date_str, sports_config):
    """
    Process a single PDF for all sports.

    Args:
        pdf_path: Path to the PDF file
        date_str: Date string in format YYYY_MM_DD
        sports_config: Dictionary defining which sports and their section indices
    """
    print(f"\n{'#'*80}")
    print(f"# PROCESSING PDF: {pdf_path}")
    print(f"# Date: {date_str}")
    print(f"{'#'*80}")

    # Create output directories
    output_dir = Path('data') / date_str
    output_dir.mkdir(parents=True, exist_ok=True)

    docs_dir = Path('docs')
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Extract text from PDF
    print("\nExtracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    print(f"✓ Extracted {len(text)} characters")

    # Process all sports based on configuration
    results = {}

    # Process football-style sports (with rushing/passing/receiving)
    for sport_name, section_index, file_prefix in sports_config.get('football_style', []):
        try:
            stats = process_football_style_sport(
                text, sport_name, section_index, file_prefix,
                date_str, output_dir, docs_dir
            )
            results[file_prefix] = stats
        except Exception as e:
            print(f"ERROR processing {sport_name}: {e}")
            import traceback
            traceback.print_exc()

    # Process soccer sports
    for sport_name, file_prefix in sports_config.get('soccer', []):
        try:
            stats = process_soccer_sport(
                text, sport_name, file_prefix,
                date_str, output_dir, docs_dir
            )
            results[file_prefix] = stats
        except Exception as e:
            print(f"ERROR processing {sport_name}: {e}")
            import traceback
            traceback.print_exc()

    # Process other sports
    if sports_config.get('volleyball', False):
        try:
            stats = process_volleyball(text, date_str, output_dir, docs_dir)
            results['volleyball'] = stats
        except Exception as e:
            print(f"ERROR processing Volleyball: {e}")
            import traceback
            traceback.print_exc()

    if sports_config.get('field_hockey', False):
        try:
            stats = process_field_hockey(text, date_str, output_dir, docs_dir)
            results['field_hockey'] = stats
        except Exception as e:
            print(f"ERROR processing Field Hockey: {e}")
            import traceback
            traceback.print_exc()

    if sports_config.get('cross_country', False):
        try:
            stats = process_cross_country(text, date_str, output_dir, docs_dir)
            results['cross_country'] = stats
        except Exception as e:
            print(f"ERROR processing Cross Country: {e}")
            import traceback
            traceback.print_exc()

    if sports_config.get('golf', False):
        try:
            stats = process_golf(text, date_str, output_dir, docs_dir)
            results['golf'] = stats
        except Exception as e:
            print(f"ERROR processing Golf: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*80}")
    print(f"✓ COMPLETED PROCESSING: {date_str}")
    print(f"{'='*80}")

    return results


def main():
    """Main processing function."""

    # October 2025 PDF configuration
    # Based on analysis: 3 INDIVIDUAL LEADERS sections
    # [0] = Volleyball (KILLS), [1] = Girls Flag Football (RUSHING), [2] = Football (RUSHING)
    october_config = {
        'football_style': [
            ("Girls Flag Football", 1, "girls_flag_football"),
            ("Football", 2, "football"),
        ],
        'soccer': [
            ("Boys Soccer", "boys_soccer"),
            ("Girls Soccer", "girls_soccer"),
        ],
        'volleyball': True,  # Process with parse_volleyball_stats
        'field_hockey': True,
        'cross_country': False,  # Not in October PDF
        'golf': True,
    }

    # December 2025 PDF configuration
    # Based on analysis: 3 INDIVIDUAL LEADERS sections
    # [0] = Girls Flag Football (RUSHING), [1] = Football (RUSHING), [2] = Volleyball (KILLS)
    december_config = {
        'football_style': [
            ("Girls Flag Football", 0, "girls_flag_football"),
            ("Football", 1, "football"),
        ],
        'soccer': [
            ("Boys Soccer", "boys_soccer"),
            ("Girls Soccer", "girls_soccer"),
        ],
        'volleyball': True,  # Process with parse_volleyball_stats
        'field_hockey': True,
        'cross_country': True,  # Rankings only - may not have player stats
        'golf': True,
    }

    # Process October 2025 PDF
    process_pdf(
        pdf_path='hs_hangout/2025_10_23.pdf',
        date_str='2025_10_23',
        sports_config=october_config
    )

    # Process December 2025 PDF
    process_pdf(
        pdf_path='hs_hangout/2025_12_06.pdf',
        date_str='2025_12_06',
        sports_config=december_config
    )

    print(f"\n{'#'*80}")
    print("# ALL PDFs PROCESSED SUCCESSFULLY!")
    print(f"{'#'*80}")
    print("\nGenerated files:")
    print("  - data/YYYY_MM_DD/ folders: JSON data and HTML files")
    print("  - docs/ folder: All HTML pages for GitHub Pages")


if __name__ == '__main__':
    main()
