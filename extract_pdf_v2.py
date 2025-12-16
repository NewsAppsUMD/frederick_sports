#!/usr/bin/env python3
"""
Improved PDF extraction script for Frederick Sports data.
Processes one PDF at a time and outputs to date-specific folders.
"""

import fitz  # PyMuPDF
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime


# Team abbreviation lookup table
TEAM_ABBREVIATIONS = {
    'Brun.': 'Brunswick',
    'Fred.': 'Frederick',
    'Ling.': 'Linganore',
    'Mid.': 'Middletown',
    'MSD': 'Maryland School for the Deaf',
    'Oak.': 'Oakdale',
    'SJCP': "St. John's Catholic Prep",
    'TJ': 'Thomas Johnson',
    'T. Johnson': 'Thomas Johnson',
    'Tus.': 'Tuscarora',
    'Walk.': 'Walkersville',
    'Catoctin': 'Catoctin',
    'Urbana': 'Urbana',
}


def expand_team_name(team_abbr: str) -> str:
    """Expand team abbreviation to full name."""
    return TEAM_ABBREVIATIONS.get(team_abbr, team_abbr)


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from the PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def find_sport_section(text: str, start_pattern: str, end_pattern: str = None, occurrence: int = 1) -> str:
    """
    Extract a specific sport section from the PDF text.

    Args:
        text: Full PDF text
        start_pattern: Starting pattern to look for (e.g., "FCPS")
        end_pattern: Optional ending pattern (next section marker)
        occurrence: Which occurrence of the pattern to use (1 = first, 2 = second, -1 = last)

    Returns:
        Section text for that sport
    """
    lines = text.split('\n')
    matches = []

    # Find all occurrences of start pattern
    for i, line in enumerate(lines):
        if start_pattern in line.strip():
            matches.append(i)

    if not matches:
        return ""

    # Select the specified occurrence
    if occurrence == -1:
        start_idx = matches[-1]
    elif occurrence > 0 and occurrence <= len(matches):
        start_idx = matches[occurrence - 1]
    else:
        return ""

    # Find end
    end_idx = len(lines)
    if end_pattern:
        for i in range(start_idx + 1, len(lines)):
            if end_pattern in lines[i].strip():
                end_idx = i
                break

    return '\n'.join(lines[start_idx:end_idx])


def parse_football_section(section_text: str) -> Dict[str, Any]:
    """
    Parse football section including standings and player stats.

    Returns:
        Dict with 'standings' and 'stats' (rushing, passing, receiving)
    """
    result = {
        'standings': {'FCPS': [], 'Other Schools': []},
        'stats': {'rushing': [], 'passing': [], 'receiving': []}
    }

    lines = section_text.split('\n')

    # Parse standings
    in_fcps_standings = False
    in_other_standings = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect FCPS standings
        if stripped == 'FCPS':
            in_fcps_standings = True
            in_other_standings = False
            continue
        elif 'OTHER SCHOOLS' in stripped or 'Other Schools' in stripped:
            in_fcps_standings = False
            in_other_standings = True
            continue
        elif 'INDIVIDUAL LEADERS' in stripped:
            in_fcps_standings = False
            in_other_standings = False
            break

        # Parse team records
        if (in_fcps_standings or in_other_standings) and stripped:
            # Skip column headers
            if stripped in ['Team', 'W', 'L', 'PF', 'PA'] or (  'W' in stripped and 'L' in stripped and 'PF' in stripped and len(stripped) < 30):
                continue

            # Split by tabs or multiple spaces
            parts = re.split(r'\t+|\s{2,}', stripped)
            # Try to find W L PF PA pattern
            if len(parts) >= 5:
                try:
                    # Last 4 elements should be numbers
                    w = int(parts[-4])
                    l = int(parts[-3])
                    pf = int(parts[-2])
                    pa = int(parts[-1])
                    team = ' '.join(parts[:-4]).strip()

                    if team:
                        team_data = {
                            'team': team,
                            'w': w,
                            'l': l,
                            'pf': pf,
                            'pa': pa
                        }

                        if in_fcps_standings:
                            result['standings']['FCPS'].append(team_data)
                        elif in_other_standings:
                            result['standings']['Other Schools'].append(team_data)
                except (ValueError, IndexError):
                    pass

    # Parse player stats
    current_stat_type = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Identify stat sections
        if 'INDIVIDUAL LEADERS' in stripped:
            continue
        elif stripped == 'RUSHING':
            current_stat_type = 'rushing'
            continue
        elif stripped == 'PASSING':
            current_stat_type = 'passing'
            continue
        elif stripped == 'RECEIVING':
            current_stat_type = 'receiving'
            continue

        # Skip headers
        if not current_stat_type:
            continue
        if 'Player, School' in stripped or 'Player' in stripped and 'School' in stripped:
            continue
        if 'Att.' in stripped or 'Yds.' in stripped or 'Avg.' in stripped:
            continue
        if 'Comp.' in stripped or 'Pct.' in stripped:
            continue
        if 'No.' in stripped or 'TD' == stripped:
            continue

        # Parse player lines - format: "Player, School\tStats..."
        if current_stat_type and ',' in stripped:
            # Split by comma to get player name and rest
            comma_idx = stripped.find(',')
            if comma_idx > 0:
                player_name = stripped[:comma_idx].strip()
                rest = stripped[comma_idx + 1:].strip()

                # Split rest by tabs/spaces to get school and stats
                parts = re.split(r'\t+', rest)
                if not parts:
                    parts = re.split(r'\s{2,}', rest)

                if len(parts) >= 2:
                    school = parts[0].strip()
                    # The rest are stats - combine and split by whitespace
                    stats_str = '\t'.join(parts[1:])
                    stats_parts = stats_str.split()

                    try:
                        if current_stat_type == 'rushing' and len(stats_parts) >= 4:
                            result['stats']['rushing'].append({
                                'player': player_name,
                                'school': expand_team_name(school),
                                'att': stats_parts[0].replace(',', ''),
                                'yds': stats_parts[1].replace(',', ''),
                                'avg': stats_parts[2],
                                'td': stats_parts[3]
                            })
                        elif current_stat_type == 'passing' and len(stats_parts) >= 5:
                            result['stats']['passing'].append({
                                'player': player_name,
                                'school': expand_team_name(school),
                                'comp': stats_parts[0],
                                'att': stats_parts[1],
                                'pct': stats_parts[2],
                                'yds': stats_parts[3].replace(',', ''),
                                'td': stats_parts[4]
                            })
                        elif current_stat_type == 'receiving' and len(stats_parts) >= 3:
                            result['stats']['receiving'].append({
                                'player': player_name,
                                'school': expand_team_name(school),
                                'rec': stats_parts[0],
                                'yds': stats_parts[1].replace(',', ''),
                                'td': stats_parts[2]
                            })
                    except (IndexError, ValueError) as e:
                        print(f"Warning: Could not parse stats for {player_name}: {e}")
                        continue

    return result


def generate_football_html(data: Dict, date_str: str) -> str:
    """Generate complete HTML page for football including standings and stats."""

    # Parse date for display
    try:
        date_obj = datetime.strptime(date_str, '%Y_%m_%d')
        display_date = date_obj.strftime('%b %d, %Y')
        # Calculate "updated through" date (2 days before publication)
        from datetime import timedelta
        updated_date = (date_obj - timedelta(days=2)).strftime('%B %d, %Y')
    except:
        display_date = date_str
        updated_date = date_str

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Football - High School Hangout ({display_date})</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 3px solid #333;
            padding-bottom: 20px;
        }}

        h1 {{
            color: #333;
            font-size: 32px;
            margin-bottom: 10px;
        }}

        .subtitle {{
            color: #666;
            font-size: 16px;
            margin: 5px 0;
        }}

        .sport-section {{
            margin: 30px 0;
        }}

        .sport-title {{
            font-size: 28px;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #666;
        }}

        .conference-title {{
            font-size: 22px;
            color: #444;
            margin: 30px 0 15px 0;
            font-weight: bold;
        }}

        .division-title {{
            font-size: 18px;
            color: #555;
            margin: 25px 0 10px 0;
            font-weight: bold;
            text-transform: uppercase;
        }}

        .section-title {{
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            margin-top: 50px;
            padding-bottom: 10px;
            border-bottom: 2px solid #666;
            text-transform: uppercase;
        }}

        .standings {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0 30px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .standings th,
        .standings td {{
            padding: 12px 10px;
            border: 1px solid #ddd;
        }}

        .standings thead th {{
            background-color: #333;
            color: white;
            font-weight: bold;
            text-align: center;
            font-size: 13px;
            letter-spacing: 0.5px;
        }}

        .standings th:first-child {{
            text-align: left;
        }}

        .standings td {{
            text-align: center;
            font-size: 14px;
        }}

        .standings td:first-child {{
            text-align: left;
            font-weight: 600;
            color: #333;
        }}

        .standings tbody tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}

        .standings tbody tr:hover {{
            background-color: #e8f4f8;
            transition: background-color 0.2s ease;
        }}

        .stats-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .stats-table th,
        .stats-table td {{
            padding: 12px 15px;
            border: 1px solid #ddd;
        }}

        .stats-table thead th {{
            background-color: #333;
            color: white;
            font-weight: bold;
            text-align: center;
            text-transform: uppercase;
            font-size: 14px;
            letter-spacing: 0.5px;
        }}

        .stats-table th:first-child,
        .stats-table th:nth-child(2) {{
            text-align: left;
        }}

        .stats-table td {{
            text-align: center;
        }}

        .stats-table td:first-child,
        .stats-table td:nth-child(2) {{
            text-align: left;
        }}

        .stats-table td:first-child {{
            font-weight: 600;
            color: #333;
        }}

        .stats-table tbody tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}

        .stats-table tbody tr:hover {{
            background-color: #e8f4f8;
            transition: background-color 0.2s ease;
        }}

        footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}

        footer p {{
            margin: 5px 0;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            .container {{
                padding: 20px;
            }}

            h1 {{
                font-size: 24px;
            }}

            .sport-title {{
                font-size: 22px;
            }}

            .division-title {{
                font-size: 16px;
            }}

            .section-title {{
                font-size: 20px;
            }}

            .standings th,
            .standings td,
            .stats-table th,
            .stats-table td {{
                padding: 8px 4px;
                font-size: 12px;
            }}
        }}

        @media print {{
            body {{
                background-color: white;
            }}

            .container {{
                box-shadow: none;
                padding: 0;
            }}

            .standings tbody tr:hover,
            .stats-table tbody tr:hover {{
                background-color: transparent;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Football - Team Standings & Individual Leaders</h1>
            <p class="subtitle">Updated Through {updated_date}</p>
            <p class="subtitle">Source: The Frederick News-Post High School Hangout</p>
        </header>

        <main>
            <!-- TEAM STANDINGS SECTION -->
            <section id="standings" class="sport-section">
                <h2 class="sport-title">Team Standings</h2>
"""

    # Add FCPS standings
    if data['standings']['FCPS']:
        html += """
                <h3 class="conference-title">FCPS</h3>
                <table class="standings">
                    <thead>
                        <tr>
                            <th>Team</th>
                            <th>W</th>
                            <th>L</th>
                            <th>PF</th>
                            <th>PA</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for team in data['standings']['FCPS']:
            html += f"""                        <tr>
                            <td>{team['team']}</td>
                            <td>{team['w']}</td>
                            <td>{team['l']}</td>
                            <td>{team['pf']}</td>
                            <td>{team['pa']}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
"""

    # Add Other Schools standings
    if data['standings']['Other Schools']:
        html += """
                <h3 class="conference-title">Other Schools</h3>
                <table class="standings">
                    <thead>
                        <tr>
                            <th>Team</th>
                            <th>W</th>
                            <th>L</th>
                            <th>PF</th>
                            <th>PA</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for team in data['standings']['Other Schools']:
            html += f"""                        <tr>
                            <td>{team['team']}</td>
                            <td>{team['w']}</td>
                            <td>{team['l']}</td>
                            <td>{team['pf']}</td>
                            <td>{team['pa']}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
"""

    html += """            </section>

            <!-- PLAYER STATS SECTION -->
            <section id="player-stats" class="sport-section">
                <h2 class="section-title">Individual Leaders</h2>
"""

    # Add rushing leaders
    if data['stats']['rushing']:
        html += """
                <!-- Rushing Leaders -->
                <div class="sport-section">
                    <h3 class="division-title">Rushing Leaders</h3>
                    <table class="stats-table">
                        <thead>
                            <tr>
                                <th>Player</th>
                                <th>School</th>
                                <th>Att</th>
                                <th>Yds</th>
                                <th>Avg</th>
                                <th>TD</th>
                            </tr>
                        </thead>
                        <tbody>
"""
        for player in data['stats']['rushing']:
            html += f"""                            <tr>
                                <td>{player['player']}</td>
                                <td>{player['school']}</td>
                                <td>{player['att']}</td>
                                <td>{player['yds']}</td>
                                <td>{player['avg']}</td>
                                <td>{player['td']}</td>
                            </tr>
"""
        html += """                        </tbody>
                    </table>
                </div>
"""

    # Add passing leaders
    if data['stats']['passing']:
        html += """
                <!-- Passing Leaders -->
                <div class="sport-section">
                    <h3 class="division-title">Passing Leaders</h3>
                    <table class="stats-table">
                        <thead>
                            <tr>
                                <th>Player</th>
                                <th>School</th>
                                <th>Comp</th>
                                <th>Att</th>
                                <th>Pct</th>
                                <th>Yds</th>
                                <th>TD</th>
                            </tr>
                        </thead>
                        <tbody>
"""
        for player in data['stats']['passing']:
            html += f"""                            <tr>
                                <td>{player['player']}</td>
                                <td>{player['school']}</td>
                                <td>{player['comp']}</td>
                                <td>{player['att']}</td>
                                <td>{player['pct']}</td>
                                <td>{player['yds']}</td>
                                <td>{player['td']}</td>
                            </tr>
"""
        html += """                        </tbody>
                    </table>
                </div>
"""

    # Add receiving leaders
    if data['stats']['receiving']:
        html += """
                <!-- Receiving Leaders -->
                <div class="sport-section">
                    <h3 class="division-title">Receiving Leaders</h3>
                    <table class="stats-table">
                        <thead>
                            <tr>
                                <th>Player</th>
                                <th>School</th>
                                <th>Rec</th>
                                <th>Yds</th>
                                <th>TD</th>
                            </tr>
                        </thead>
                        <tbody>
"""
        for player in data['stats']['receiving']:
            html += f"""                            <tr>
                                <td>{player['player']}</td>
                                <td>{player['school']}</td>
                                <td>{player['rec']}</td>
                                <td>{player['yds']}</td>
                                <td>{player['td']}</td>
                            </tr>
"""
        html += """                        </tbody>
                    </table>
                </div>
"""

    html += """            </section>
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


def process_pdf(pdf_path: str, date_str: str):
    """
    Process a single PDF and generate all output files.

    Args:
        pdf_path: Path to the PDF file
        date_str: Date string in format YYYY_MM_DD
    """
    print(f"\n{'='*70}")
    print(f"Processing PDF: {pdf_path}")
    print(f"Date: {date_str}")
    print(f"{'='*70}\n")

    # Create output directory
    output_dir = Path('data') / date_str
    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract text
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)

    # Save full text
    text_file = output_dir / 'full_text.txt'
    with open(text_file, 'w') as f:
        f.write(text)
    print(f"Saved full text to: {text_file}")

    # Process Football (boys) - This is the SECOND "FCPS" section
    print("\n" + "="*70)
    print("Processing FOOTBALL (Boys)")
    print("="*70)

    # Find the second FCPS section (first is Girls Flag Football)
    football_section = find_sport_section(text, "FCPS", occurrence=2)
    if football_section:
        football_data = parse_football_section(football_section)

        # Save JSON data
        json_file = output_dir / 'football_data.json'
        with open(json_file, 'w') as f:
            json.dump(football_data, f, indent=2)
        print(f"Saved football data to: {json_file}")

        # Print stats
        print(f"\nFootball stats parsed:")
        print(f"  FCPS teams: {len(football_data['standings']['FCPS'])}")
        print(f"  Other Schools: {len(football_data['standings']['Other Schools'])}")
        print(f"  Rushing leaders: {len(football_data['stats']['rushing'])}")
        print(f"  Passing leaders: {len(football_data['stats']['passing'])}")
        print(f"  Receiving leaders: {len(football_data['stats']['receiving'])}")

        # Generate HTML
        html = generate_football_html(football_data, date_str)
        html_file = output_dir / 'football.html'
        with open(html_file, 'w') as f:
            f.write(html)
        print(f"Saved football HTML to: {html_file}")
    else:
        print("WARNING: Could not find FOOTBALL section in PDF")

    print(f"\n{'='*70}")
    print(f"Processing complete for {date_str}")
    print(f"All files saved to: {output_dir}")
    print(f"{'='*70}\n")


def main():
    """Main function."""
    if len(sys.argv) > 1:
        # Process specified PDF
        pdf_path = sys.argv[1]
        if len(sys.argv) > 2:
            date_str = sys.argv[2]
        else:
            # Extract date from filename
            filename = Path(pdf_path).stem
            date_str = filename if '_' in filename else 'unknown'

        process_pdf(pdf_path, date_str)
    else:
        # Process all PDFs
        pdfs = [
            ('hs_hangout/2025_10_23.pdf', '2025_10_23'),
            ('hs_hangout/2025_12_06.pdf', '2025_12_06')
        ]

        for pdf_path, date_str in pdfs:
            if Path(pdf_path).exists():
                process_pdf(pdf_path, date_str)
            else:
                print(f"WARNING: PDF not found: {pdf_path}")


if __name__ == '__main__':
    main()
