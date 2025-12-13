#!/usr/bin/env python3
"""
Create combined standings + stats HTML files for December 6, 2025
Combines October standings with December player stats
"""

import re
from pathlib import Path

def extract_standings_section(html_content):
    """Extract the standings section from HTML"""
    # Find the standings section
    start_marker = '<!-- TEAM STANDINGS SECTION -->'
    end_marker = '<!-- PLAYER STATS SECTION -->'

    start = html_content.find(start_marker)
    end = html_content.find(end_marker)

    if start == -1 or end == -1:
        return None

    return html_content[start:end]

def extract_player_stats_section(html_content):
    """Extract player stats from player_stats HTML file"""
    # Find the main section content
    start_marker = '<main>'
    end_marker = '</main>'

    start = html_content.find(start_marker)
    end = html_content.find(end_marker)

    if start == -1 or end == -1:
        return None

    # Get the content between <main> tags
    main_content = html_content[start + len(start_marker):end].strip()

    # Wrap in player stats section
    return f'''
            <!-- PLAYER STATS SECTION -->
            <section id="player-stats" class="sport-section">
                <h2 class="section-title">Individual Leaders</h2>
{main_content}
            </section>'''

def create_combined_file(sport_name, oct_combined_path, dec_stats_path, output_path, display_name=None):
    """Create a combined HTML file with October standings and December stats"""

    if display_name is None:
        display_name = sport_name

    print(f"Creating combined file for {sport_name}...")

    # Read October combined file
    with open(oct_combined_path, 'r') as f:
        oct_html = f.read()

    # Read December player stats file
    with open(dec_stats_path, 'r') as f:
        dec_html = f.read()

    # Extract sections
    standings = extract_standings_section(oct_html)
    player_stats = extract_player_stats_section(dec_html)

    if not standings:
        print(f"  WARNING: Could not extract standings from {oct_combined_path}")
        return False

    if not player_stats:
        print(f"  WARNING: Could not extract player stats from {dec_stats_path}")
        return False

    # Get the template from October file (up to standings section)
    template_end = oct_html.find('<!-- TEAM STANDINGS SECTION -->')
    template_start = oct_html[:template_end]

    # Get footer from October file
    footer_start = oct_html.find('<footer>')
    footer = oct_html[footer_start:]

    # Update dates in template
    template_start = template_start.replace('(Oct 23, 2025)', '(Dec 6, 2025)')
    template_start = template_start.replace('October 21, 2025', 'December 4, 2025')

    # Combine everything
    combined_html = template_start + standings + player_stats + '''
        </main>

        ''' + footer

    # Write output file
    with open(output_path, 'w') as f:
        f.write(combined_html)

    print(f"  ✓ Created {output_path}")
    return True

def main():
    # Base directories
    hs_hangout = Path('hs_hangout')
    docs = Path('docs')

    # Sports to process (those that have December data)
    sports = [
        ('girls_flag_football', 'Girls Flag Football'),
        ('boys_soccer', 'Boys Soccer'),
        ('girls_soccer', 'Girls Soccer'),
        ('volleyball', 'Volleyball'),
        ('field_hockey', 'Field Hockey'),
    ]

    for sport_key, sport_name in sports:
        # Paths
        oct_combined = hs_hangout / f'{sport_key}_2025_10_23.html'
        dec_stats = hs_hangout / f'player_stats_{sport_key}_2025_12_06.html'
        output_hs = hs_hangout / f'{sport_key}_2025_12_06.html'
        output_docs = docs / f'{sport_key}_2025_12_06.html'

        if not oct_combined.exists():
            print(f"Skipping {sport_name}: October combined file not found")
            continue

        if not dec_stats.exists():
            print(f"Skipping {sport_name}: December stats file not found")
            continue

        # Create combined file in hs_hangout
        success = create_combined_file(sport_name, oct_combined, dec_stats, output_hs, sport_name)

        if success:
            # Copy to docs
            with open(output_hs, 'r') as f:
                content = f.read()
            with open(output_docs, 'w') as f:
                f.write(content)
            print(f"  ✓ Copied to {output_docs}")

    print("\n✓ All combined files created!")

if __name__ == '__main__':
    main()
