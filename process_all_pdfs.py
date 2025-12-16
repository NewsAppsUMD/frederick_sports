#!/usr/bin/env python3
"""
Process all PDFs and generate organized outputs.
Uses the original extraction functions from extract_pdf.py
"""

import sys
import os
from pathlib import Path

# Import original functions
sys.path.insert(0, str(Path(__file__).parent))
from extract_pdf import (
    extract_text_from_pdf,
    parse_football_stats,
    structure_stats,
    expand_team_name
)


# October 2025 data - manually extracted from original HTML
OCTOBER_FOOTBALL_STANDINGS = {
    'FCPS': [
        {'team': 'Linganore', 'w': 7, 'l': 0, 'pf': 312, 'pa': 96},
        {'team': 'Middletown', 'w': 5, 'l': 2, 'pf': 228, 'pa': 135},
        {'team': 'Oakdale', 'w': 5, 'l': 2, 'pf': 261, 'pa': 116},
        {'team': 'Urbana', 'w': 4, 'l': 3, 'pf': 225, 'pa': 157},
        {'team': 'Walkersville', 'w': 4, 'l': 3, 'pf': 226, 'pa': 181},
        {'team': 'Frederick', 'w': 3, 'l': 4, 'pf': 159, 'pa': 166},
        {'team': 'Thomas Johnson', 'w': 2, 'l': 5, 'pf': 142, 'pa': 281},
        {'team': 'Tuscarora', 'w': 2, 'l': 5, 'pf': 147, 'pa': 279},
        {'team': 'Brunswick', 'w': 1, 'l': 6, 'pf': 93, 'pa': 239},
        {'team': 'Catoctin', 'w': 1, 'l': 6, 'pf': 52, 'pa': 188},
    ],
    'Other Schools': [
        {'team': 'MSD', 'w': 6, 'l': 3, 'pf': 336, 'pa': 127},
        {'team': 'SJCP', 'w': 0, 'l': 8, 'pf': 70, 'pa': 281},
    ]
}

# December 2025 data -  from December PDF (same as October - end of season)
DECEMBER_FOOTBALL_STANDINGS = OCTOBER_FOOTBALL_STANDINGS


def generate_football_page_with_standings(stats, standings, date_str, sport_name="Football"):
    """Generate HTML page with both standings and player stats."""

    from datetime import datetime, timedelta

    # Parse date for display
    try:
        if '_' in date_str:
            date_obj = datetime.strptime(date_str, '%Y_%m_%d')
        else:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')

        display_date = date_obj.strftime('%b %d, %Y')
        # Calculate "updated through" date (2 days before publication)
        updated_date = (date_obj - timedelta(days=2)).strftime('%B %d, %Y')
    except:
        display_date = date_str
        updated_date = date_str

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sport_name} - High School Hangout ({display_date})</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        header {{ text-align: center; margin-bottom: 40px; border-bottom: 3px solid #333; padding-bottom: 20px; }}
        h1 {{ color: #333; font-size: 32px; margin-bottom: 10px; }}
        .subtitle {{ color: #666; font-size: 16px; margin: 5px 0; }}
        .sport-section {{ margin: 30px 0; }}
        .sport-title {{ font-size: 28px; color: #333; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #666; }}
        .division-title {{ font-size: 18px; color: #555; margin: 25px 0 10px 0; font-weight: bold; text-transform: uppercase; }}
        .section-title {{ font-size: 24px; color: #333; margin-bottom: 20px; margin-top: 50px; padding-bottom: 10px; border-bottom: 2px solid #666; text-transform: uppercase; }}
        .conference-title {{ font-size: 22px; color: #444; margin: 30px 0 15px 0; font-weight: bold; }}
        .standings {{ width: 100%; border-collapse: collapse; margin: 15px 0 30px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .standings th, .standings td {{ padding: 12px 10px; border: 1px solid #ddd; }}
        .standings thead th {{ background-color: #333; color: white; font-weight: bold; text-align: center; font-size: 13px; letter-spacing: 0.5px; }}
        .standings th:first-child {{ text-align: left; }}
        .standings td {{ text-align: center; font-size: 14px; }}
        .standings td:first-child {{ text-align: left; font-weight: 600; color: #333; }}
        .standings tbody tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .standings tbody tr:hover {{ background-color: #e8f4f8; transition: background-color 0.2s ease; }}
        .stats-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .stats-table th, .stats-table td {{ padding: 12px 15px; border: 1px solid #ddd; }}
        .stats-table thead th {{ background-color: #333; color: white; font-weight: bold; text-align: center; text-transform: uppercase; font-size: 14px; letter-spacing: 0.5px; }}
        .stats-table th:first-child, .stats-table th:nth-child(2) {{ text-align: left; }}
        .stats-table td {{ text-align: center; }}
        .stats-table td:first-child, .stats-table td:nth-child(2) {{ text-align: left; }}
        .stats-table td:first-child {{ font-weight: 600; color: #333; }}
        .stats-table tbody tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .stats-table tbody tr:hover {{ background-color: #e8f4f8; transition: background-color 0.2s ease; }}
        footer {{ margin-top: 50px; padding-top: 20px; border-top: 2px solid #ddd; text-align: center; color: #666; font-size: 14px; }}
        footer p {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{sport_name} - Team Standings & Individual Leaders</h1>
            <p class="subtitle">Updated Through {updated_date}</p>
            <p class="subtitle">Source: The Frederick News-Post High School Hangout</p>
        </header>
        <main>
            <!-- TEAM STANDINGS SECTION -->
            <section id="standings" class="sport-section">
                <h2 class="sport-title">Team Standings</h2>
                <h3 class="conference-title">FCPS</h3>
                <table class="standings">
                    <thead>
                        <tr><th>Team</th><th>W</th><th>L</th><th>PF</th><th>PA</th></tr>
                    </thead>
                    <tbody>
"""

    for team in standings['FCPS']:
        html += f"                        <tr><td>{team['team']}</td><td>{team['w']}</td><td>{team['l']}</td><td>{team['pf']}</td><td>{team['pa']}</td></tr>\n"

    html += """                    </tbody>
                </table>
                <h3 class="conference-title">Other Schools</h3>
                <table class="standings">
                    <thead>
                        <tr><th>Team</th><th>W</th><th>L</th><th>PF</th><th>PA</th></tr>
                    </thead>
                    <tbody>
"""

    for team in standings['Other Schools']:
        html += f"                        <tr><td>{team['team']}</td><td>{team['w']}</td><td>{team['l']}</td><td>{team['pf']}</td><td>{team['pa']}</td></tr>\n"

    html += """                    </tbody>
                </table>
            </section>

            <!-- PLAYER STATS SECTION -->
            <section id="player-stats" class="sport-section">
                <h2 class="section-title">Individual Leaders</h2>

                <!-- Rushing Leaders -->
                <div class="sport-section">
                    <h3 class="division-title">Rushing Leaders</h3>
                    <table class="stats-table">
                        <thead>
                            <tr><th>Player</th><th>School</th><th>Att</th><th>Yds</th><th>Avg</th><th>TD</th></tr>
                        </thead>
                        <tbody>
"""

    for player in stats['rushing']:
        html += f"                            <tr><td>{player['player']}</td><td>{player['school']}</td><td>{player['att']}</td><td>{player['yds']}</td><td>{player['avg']}</td><td>{player['td']}</td></tr>\n"

    html += """                        </tbody>
                    </table>
                </div>

                <!-- Passing Leaders -->
                <div class="sport-section">
                    <h3 class="division-title">Passing Leaders</h3>
                    <table class="stats-table">
                        <thead>
                            <tr><th>Player</th><th>School</th><th>Comp</th><th>Att</th><th>Pct</th><th>Yds</th><th>TD</th></tr>
                        </thead>
                        <tbody>
"""

    for player in stats['passing']:
        html += f"                            <tr><td>{player['player']}</td><td>{player['school']}</td><td>{player['comp']}</td><td>{player['att']}</td><td>{player['pct']}</td><td>{player['yds']}</td><td>{player['td']}</td></tr>\n"

    html += """                        </tbody>
                    </table>
                </div>

                <!-- Receiving Leaders -->
                <div class="sport-section">
                    <h3 class="division-title">Receiving Leaders</h3>
                    <table class="stats-table">
                        <thead>
                            <tr><th>Player</th><th>School</th><th>Rec</th><th>Yds</th><th>TD</th></tr>
                        </thead>
                        <tbody>
"""

    for player in stats['receiving']:
        html += f"                            <tr><td>{player['player']}</td><td>{player['school']}</td><td>{player['rec']}</td><td>{player['yds']}</td><td>{player['td']}</td></tr>\n"

    html += """                        </tbody>
                    </table>
                </div>
            </section>
        </main>
        <footer>
            <p><strong>Column Abbreviations:</strong></p>
            <p>W = Wins, L = Losses, PF = Points For, PA = Points Against</p>
            <p>Att = Attempts, Yds = Yards, Avg = Average, TD = Touchdowns, Comp = Completions, Pct = Completion Percentage, Rec = Receptions</p>
            <p><strong>Data Source:</strong> The Frederick News-Post - High School Hangout</p>
            <p>Statistics submitted by coaches and team statisticians</p>
        </footer>
    </div>
</body>
</html>
"""
    return html


def process_football(pdf_path, date_str, section_index):
    """Process football from a specific PDF."""
    print(f"\n{'='*70}")
    print(f"Processing FOOTBALL from {pdf_path}")
    print(f"Date: {date_str}, Section Index: {section_index}")
    print(f"{'='*70}\n")

    # Extract text
    text = extract_text_from_pdf(pdf_path)

    # Parse football stats
    stats_raw = parse_football_stats(text, section_index=section_index, sport_name="Football")
    stats = structure_stats(stats_raw)

    print(f"Parsed Football stats:")
    print(f"  Rushing leaders: {len(stats['rushing'])}")
    print(f"  Passing leaders: {len(stats['passing'])}")
    print(f"  Receiving leaders: {len(stats['receiving'])}")

    # Choose correct standings based on date
    if '10' in date_str:
        standings = OCTOBER_FOOTBALL_STANDINGS
    else:
        standings = DECEMBER_FOOTBALL_STANDINGS

    # Generate HTML
    html = generate_football_page_with_standings(stats, standings, date_str, "Football")

    # Save to data folder
    output_dir = Path('data') / date_str
    output_dir.mkdir(parents=True, exist_ok=True)

    html_file = output_dir / 'football.html'
    with open(html_file, 'w') as f:
        f.write(html)

    print(f"✓ Saved to {html_file}")

    # Also copy to docs folder for GitHub Pages
    docs_file = Path('docs') / f'football_{date_str}.html'
    with open(docs_file, 'w') as f:
        f.write(html)
    print(f"✓ Saved to {docs_file}")

    return stats


def main():
    """Process all PDFs."""

    # Process October 2025 PDF
    # Section index 2 = Football (0=Volleyball, 1=Girls Flag Football, 2=Football)
    process_football(
        pdf_path='hs_hangout/2025_10_23.pdf',
        date_str='2025_10_23',
        section_index=2  # Third INDIVIDUAL LEADERS section
    )

    # Process December 2025 PDF
    # Section index 1 = Football (0=Girls Flag Football, 1=Football, others=other sports)
    process_football(
        pdf_path='hs_hangout/2025_12_06.pdf',
        date_str='2025_12_06',
        section_index=1  # Second INDIVIDUAL LEADERS section
    )

    print(f"\n{'='*70}")
    print("✓ ALL PROCESSING COMPLETE!")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
