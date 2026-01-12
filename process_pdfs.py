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
    # Standings parsing functions
    parse_fcps_standings,
    parse_central_maryland_standings,
    parse_other_schools_standings,
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


def get_dates_for_pdf(date_str):
    """
    Get formatted publish and update dates for a given PDF date string.

    Args:
        date_str: Date string in format YYYY_MM_DD

    Returns:
        Tuple of (publish_date, updated_date)
    """
    date_mapping = {
        '2025_10_23': ('Oct 23, 2025', 'October 21, 2025'),
        '2025_12_06': ('Dec. 6, 2025', 'December 4, 2025'),
    }
    return date_mapping.get(date_str, ('Oct 23, 2025', 'October 21, 2025'))


def process_football_style_sport(text, sport_name, section_index, file_prefix, date_str, output_dir, docs_dir, fcps_standings_index=0):
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

    # Parse FCPS standings
    print(f"Parsing FCPS standings (section {fcps_standings_index})...")
    standings = parse_fcps_standings(text, section_index=fcps_standings_index)
    print(f"  FCPS standings: {len(standings)} teams")

    # Save standings to JSON
    standings_data = {'fcps': standings}
    standings_json_file = output_dir / f'{file_prefix}_standings.json'
    with open(standings_json_file, 'w') as f:
        json.dump(standings_data, f, indent=2)
    print(f"✓ Saved standings JSON to {standings_json_file}")

    # Generate HTML
    print(f"Generating HTML page...")
    publish_date, updated_date = get_dates_for_pdf(date_str)
    html = generate_html(stats, sport_name, defensive_stats, publish_date, updated_date, standings)

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


def process_soccer_sport(text, sport_name, file_prefix, date_str, output_dir, docs_dir, cmc_standings_index=0):
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

    # Parse Central Maryland Conference standings
    print(f"Parsing Central Maryland Conference standings (section {cmc_standings_index})...")
    standings = parse_central_maryland_standings(text, sport_name, section_index=cmc_standings_index)
    if standings:
        total_teams = sum(len(teams) for teams in standings.values())
        print(f"  Central Maryland standings: {len(standings)} divisions, {total_teams} teams")

    # Parse Other Schools standings if present (search after the CMC section)
    lines = text.split('\n')
    cmc_sections = [i for i, line in enumerate(lines) if 'CENTRAL MARYLAND CONFERENCE' in line]
    after_line = cmc_sections[cmc_standings_index] if cmc_standings_index < len(cmc_sections) else 0
    other_schools = parse_other_schools_standings(text, after_line=after_line)
    if other_schools:
        standings['OTHER SCHOOLS'] = other_schools
        print(f"  Other Schools: {len(other_schools)} teams")

    # Save standings to JSON
    standings_json_file = output_dir / f'{file_prefix}_standings.json'
    with open(standings_json_file, 'w') as f:
        json.dump(standings, f, indent=2)
    print(f"✓ Saved standings JSON to {standings_json_file}")

    # Generate HTML
    print(f"Generating HTML page...")
    publish_date, updated_date = get_dates_for_pdf(date_str)
    html = generate_soccer_html(stats, sport_name, publish_date, updated_date, standings)

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


def process_volleyball(text, date_str, output_dir, docs_dir, cmc_standings_index=0):
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

    # Parse Central Maryland Conference standings
    print(f"Parsing Central Maryland Conference standings (section {cmc_standings_index})...")
    standings = parse_central_maryland_standings(text, sport_name, section_index=cmc_standings_index)
    if standings:
        total_teams = sum(len(teams) for teams in standings.values())
        print(f"  Central Maryland standings: {len(standings)} divisions, {total_teams} teams")

    # Parse Other Schools standings if present (search after the CMC section)
    lines = text.split('\n')
    cmc_sections = [i for i, line in enumerate(lines) if 'CENTRAL MARYLAND CONFERENCE' in line]
    after_line = cmc_sections[cmc_standings_index] if cmc_standings_index < len(cmc_sections) else 0
    other_schools = parse_other_schools_standings(text, after_line=after_line)
    if other_schools:
        standings['OTHER SCHOOLS'] = other_schools
        print(f"  Other Schools: {len(other_schools)} teams")

    # Save standings to JSON
    standings_json_file = output_dir / f'{file_prefix}_standings.json'
    with open(standings_json_file, 'w') as f:
        json.dump(standings, f, indent=2)
    print(f"✓ Saved standings JSON to {standings_json_file}")

    # Generate HTML
    print(f"Generating HTML page...")
    publish_date, updated_date = get_dates_for_pdf(date_str)
    html = generate_volleyball_html(stats, sport_name, publish_date, updated_date, standings)

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


def process_field_hockey(text, date_str, output_dir, docs_dir, cmc_standings_index=0):
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

    # Parse Central Maryland Conference standings
    print(f"Parsing Central Maryland Conference standings (section {cmc_standings_index})...")
    standings = parse_central_maryland_standings(text, sport_name, section_index=cmc_standings_index)
    if standings:
        total_teams = sum(len(teams) for teams in standings.values())
        print(f"  Central Maryland standings: {len(standings)} divisions, {total_teams} teams")

    # Parse Other Schools standings if present (search after the CMC section)
    lines = text.split('\n')
    cmc_sections = [i for i, line in enumerate(lines) if 'CENTRAL MARYLAND CONFERENCE' in line]
    after_line = cmc_sections[cmc_standings_index] if cmc_standings_index < len(cmc_sections) else 0
    other_schools = parse_other_schools_standings(text, after_line=after_line)
    if other_schools:
        standings['OTHER SCHOOLS'] = other_schools
        print(f"  Other Schools: {len(other_schools)} teams")

    # Save standings to JSON
    standings_json_file = output_dir / f'{file_prefix}_standings.json'
    with open(standings_json_file, 'w') as f:
        json.dump(standings, f, indent=2)
    print(f"✓ Saved standings JSON to {standings_json_file}")

    # Generate HTML
    print(f"Generating HTML page...")
    publish_date, updated_date = get_dates_for_pdf(date_str)
    html = generate_field_hockey_html(stats, sport_name, publish_date, updated_date, standings)

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
    publish_date, updated_date = get_dates_for_pdf(date_str)
    html = generate_cross_country_html(stats, sport_name, publish_date, updated_date)

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
    publish_date, updated_date = get_dates_for_pdf(date_str)
    html = generate_golf_html(stats, sport_name, publish_date, updated_date)

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
    for sport_tuple in sports_config.get('football_style', []):
        sport_name, section_index, file_prefix, fcps_standings_index = sport_tuple
        try:
            stats = process_football_style_sport(
                text, sport_name, section_index, file_prefix,
                date_str, output_dir, docs_dir,
                fcps_standings_index=fcps_standings_index
            )
            results[file_prefix] = stats
        except Exception as e:
            print(f"ERROR processing {sport_name}: {e}")
            import traceback
            traceback.print_exc()

    # Process soccer sports
    for sport_tuple in sports_config.get('soccer', []):
        sport_name, file_prefix, cmc_standings_index = sport_tuple
        try:
            stats = process_soccer_sport(
                text, sport_name, file_prefix,
                date_str, output_dir, docs_dir,
                cmc_standings_index=cmc_standings_index
            )
            results[file_prefix] = stats
        except Exception as e:
            print(f"ERROR processing {sport_name}: {e}")
            import traceback
            traceback.print_exc()

    # Process other sports
    volleyball_config = sports_config.get('volleyball', False)
    if volleyball_config:
        try:
            cmc_index = volleyball_config.get('cmc_standings_index', 0) if isinstance(volleyball_config, dict) else 0
            stats = process_volleyball(text, date_str, output_dir, docs_dir, cmc_standings_index=cmc_index)
            results['volleyball'] = stats
        except Exception as e:
            print(f"ERROR processing Volleyball: {e}")
            import traceback
            traceback.print_exc()

    field_hockey_config = sports_config.get('field_hockey', False)
    if field_hockey_config:
        try:
            cmc_index = field_hockey_config.get('cmc_standings_index', 0) if isinstance(field_hockey_config, dict) else 0
            stats = process_field_hockey(text, date_str, output_dir, docs_dir, cmc_standings_index=cmc_index)
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
    # FCPS standings: [0] = Girls Flag Football, [1] = Football
    # CMC standings: [0] = Volleyball, [1] = Field Hockey, [2] = Boys Soccer, [3] = Girls Soccer
    october_config = {
        'football_style': [
            # (sport_name, stats_section_index, file_prefix, fcps_standings_index)
            ("Girls Flag Football", 1, "girls_flag_football", 0),
            ("Football", 2, "football", 1),
        ],
        'soccer': [
            # (sport_name, file_prefix, cmc_standings_index)
            ("Boys Soccer", "boys_soccer", 2),
            ("Girls Soccer", "girls_soccer", 3),
        ],
        'volleyball': {'enabled': True, 'cmc_standings_index': 0},
        'field_hockey': {'enabled': True, 'cmc_standings_index': 1},
        'cross_country': True,  # Process cross country
        'golf': True,
    }

    # December 2025 PDF configuration
    # Based on analysis: 3 INDIVIDUAL LEADERS sections
    # [0] = Girls Flag Football (RUSHING), [1] = Football (RUSHING), [2] = Volleyball (KILLS)
    # FCPS standings: [0] = Girls Flag Football, [1] = Football
    # CMC standings: [0] = Field Hockey, [1] = Volleyball, [2] = Girls Soccer, [3] = Boys Soccer
    december_config = {
        'football_style': [
            # (sport_name, stats_section_index, file_prefix, fcps_standings_index)
            ("Girls Flag Football", 0, "girls_flag_football", 0),
            ("Football", 1, "football", 1),
        ],
        'soccer': [
            # (sport_name, file_prefix, cmc_standings_index)
            ("Boys Soccer", "boys_soccer", 3),
            ("Girls Soccer", "girls_soccer", 2),
        ],
        'volleyball': {'enabled': True, 'cmc_standings_index': 1},
        'field_hockey': {'enabled': True, 'cmc_standings_index': 0},
        'cross_country': True,  # Has individual runner times
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
