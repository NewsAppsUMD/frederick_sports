#!/usr/bin/env python3
"""
PDF extraction script for Frederick Sports player statistics.
Extracts player stats from the HS Hangout PDF and converts to structured data.
"""

import fitz  # PyMuPDF
import re
import json
from typing import Dict, List, Any, Tuple


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from the PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def parse_football_stats(text: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Parse football player statistics from extracted text.
    Returns dict with keys: rushing, passing, receiving
    """
    stats = {
        'rushing': [],
        'passing': [],
        'receiving': []
    }

    # Split text into lines for easier parsing
    lines = text.split('\n')

    # Find ALL occurrences of INDIVIDUAL LEADERS sections
    # We want the LAST one (Boys Football) not the first one (Girls Flag Football)
    individual_leaders_indices = []
    for i, line in enumerate(lines):
        if line.strip() == 'INDIVIDUAL LEADERS':
            individual_leaders_indices.append(i)

    if not individual_leaders_indices:
        print("DEBUG: No INDIVIDUAL LEADERS sections found")
        return stats

    # Use the last INDIVIDUAL LEADERS section (Boys Football)
    start_idx = individual_leaders_indices[-1]
    print(f"DEBUG: Found {len(individual_leaders_indices)} INDIVIDUAL LEADERS sections")
    print(f"DEBUG: Using last one at line {start_idx}")

    current_section = None
    current_player_lines = []

    def save_current_player():
        """Save accumulated player lines as one entry."""
        if current_player_lines:
            # Combine all lines with tab separator
            combined = '\t'.join(current_player_lines)
            stats[current_section].append({'raw': combined})
            current_player_lines.clear()

    for i in range(start_idx, len(lines)):
        stripped = lines[i].strip()

        # Identify section headers
        if stripped == 'RUSHING':
            save_current_player()
            current_section = 'rushing'
            print(f"DEBUG: Found RUSHING section at line {i}")
            continue
        elif stripped == 'PASSING':
            save_current_player()
            current_section = 'passing'
            print(f"DEBUG: Found PASSING section at line {i}")
            continue
        elif stripped == 'RECEIVING':
            save_current_player()
            current_section = 'receiving'
            print(f"DEBUG: Found RECEIVING section at line {i}")
            continue

        # Stop at empty line followed by non-data (end of stats)
        if current_section == 'receiving' and stripped == '':
            # Check if we've hit the end
            if i + 1 < len(lines) and lines[i+1].strip() == '':
                save_current_player()
                break

        # Parse player data
        if current_section and stripped:
            # Skip column header lines
            if 'Player, School' in stripped or 'Att.' in stripped or 'Yds.' in stripped:
                continue
            if 'Comp.' in stripped or 'No.' in stripped or 'Pct.' in stripped:
                continue
            if 'Player' in stripped and 'School' in stripped:
                continue
            if 'Avg.' in stripped or 'TD' in stripped:
                continue

            # Check if this is a new player entry (contains comma)
            if ',' in stripped:
                # Save previous player
                save_current_player()
                # Start new player
                current_player_lines.append(stripped)
            elif current_player_lines:
                # This is a continuation of the current player's data
                current_player_lines.append(stripped)

    # Save any remaining player
    save_current_player()

    return stats


def parse_player_entry(raw: str, stat_type: str) -> Dict[str, Any]:
    """
    Parse a raw player entry into structured data.

    Args:
        raw: Raw text like "Player Name, School\tStat1\tStat2..."
        stat_type: Type of stats ('rushing', 'passing', 'receiving')

    Returns:
        Dict with player name, school, and stats
    """
    # Split by comma to separate name and rest
    if ',' not in raw:
        return None

    parts = raw.split(',', 1)
    player_name = parts[0].strip()
    rest = parts[1].strip()

    # Split rest by tabs/spaces to get school and stats
    tokens = re.split(r'[\t]+', rest)
    tokens = [t.strip() for t in tokens if t.strip()]

    if not tokens:
        return None

    school = tokens[0]
    stats_values = tokens[1:] if len(tokens) > 1 else []

    result = {
        'player': player_name,
        'school': school
    }

    # Parse stats based on type
    if stat_type == 'rushing':
        # Rushing: Att, Yds, Avg, TD
        if len(stats_values) >= 1:
            result['att'] = stats_values[0]
        if len(stats_values) >= 2:
            result['yds'] = stats_values[1]
        if len(stats_values) >= 3:
            result['avg'] = stats_values[2]
        if len(stats_values) >= 4:
            result['td'] = stats_values[3]
    elif stat_type == 'passing':
        # Passing: Comp, Att, Pct, Yds, TD
        if len(stats_values) >= 1:
            result['comp'] = stats_values[0]
        if len(stats_values) >= 2:
            result['att'] = stats_values[1]
        if len(stats_values) >= 3:
            result['pct'] = stats_values[2]
        if len(stats_values) >= 4:
            result['yds'] = stats_values[3]
        if len(stats_values) >= 5:
            result['td'] = stats_values[4]
    elif stat_type == 'receiving':
        # Receiving: No, Yds, TD
        if len(stats_values) >= 1:
            result['rec'] = stats_values[0]
        if len(stats_values) >= 2:
            result['yds'] = stats_values[1]
        if len(stats_values) >= 3:
            result['td'] = stats_values[2]

    return result


def structure_stats(raw_stats: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
    """Convert raw stats to structured format."""
    structured = {
        'rushing': [],
        'passing': [],
        'receiving': []
    }

    for stat_type in ['rushing', 'passing', 'receiving']:
        for entry in raw_stats[stat_type]:
            parsed = parse_player_entry(entry['raw'], stat_type)
            if parsed:
                structured[stat_type].append(parsed)

    return structured


def generate_html(stats: Dict[str, List[Dict]], sport: str = "Football") -> str:
    """Generate HTML page for player stats."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sport} Player Stats - High School Hangout (Oct 23, 2025)</title>
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

        .section-title {{
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #666;
            text-transform: uppercase;
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

        /* Responsive design */
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

            .section-title {{
                font-size: 20px;
            }}

            .stats-table th,
            .stats-table td {{
                padding: 8px 10px;
                font-size: 14px;
            }}
        }}

        @media print {{
            body {{
                background-color: white;
                padding: 0;
            }}

            .container {{
                box-shadow: none;
            }}

            .stats-table tbody tr:hover {{
                background-color: inherit;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{sport} Individual Leaders</h1>
            <p class="subtitle">Updated Through October 21, 2025</p>
            <p class="subtitle">Source: The Frederick News-Post High School Hangout</p>
        </header>

        <main>
"""

    # Rushing Leaders
    if stats.get('rushing'):
        html += """
            <div class="sport-section">
                <h2 class="section-title">Rushing Leaders</h2>
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
        for player in stats['rushing']:
            html += f"""                        <tr>
                            <td>{player.get('player', '')}</td>
                            <td>{player.get('school', '')}</td>
                            <td>{player.get('att', '')}</td>
                            <td>{player.get('yds', '')}</td>
                            <td>{player.get('avg', '')}</td>
                            <td>{player.get('td', '')}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
            </div>
"""

    # Passing Leaders
    if stats.get('passing'):
        html += """
            <div class="sport-section">
                <h2 class="section-title">Passing Leaders</h2>
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
        for player in stats['passing']:
            html += f"""                        <tr>
                            <td>{player.get('player', '')}</td>
                            <td>{player.get('school', '')}</td>
                            <td>{player.get('comp', '')}</td>
                            <td>{player.get('att', '')}</td>
                            <td>{player.get('pct', '')}</td>
                            <td>{player.get('yds', '')}</td>
                            <td>{player.get('td', '')}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
            </div>
"""

    # Receiving Leaders
    if stats.get('receiving'):
        html += """
            <div class="sport-section">
                <h2 class="section-title">Receiving Leaders</h2>
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
        for player in stats['receiving']:
            html += f"""                        <tr>
                            <td>{player.get('player', '')}</td>
                            <td>{player.get('school', '')}</td>
                            <td>{player.get('rec', '')}</td>
                            <td>{player.get('yds', '')}</td>
                            <td>{player.get('td', '')}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
            </div>
"""

    html += """
        </main>

        <footer>
            <p><strong>Column Abbreviations:</strong></p>
            <p>Att = Attempts, Yds = Yards, Avg = Average, TD = Touchdowns, Comp = Completions, Pct = Completion Percentage, Rec = Receptions</p>
            <p><strong>Data Source:</strong> The Frederick News-Post - High School Hangout</p>
            <p>Statistics submitted by coaches and team statisticians</p>
        </footer>
    </div>
</body>
</html>
"""

    return html


def main():
    """Main extraction function."""
    pdf_path = '/home/user/frederick_sports/hs_hangout/2025_10_23.pdf'

    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)

    # Save full text for inspection
    with open('/home/user/frederick_sports/pdf_text.txt', 'w') as f:
        f.write(text)
    print(f"Full text saved to pdf_text.txt ({len(text)} characters)")

    # Parse football stats
    print("\nParsing football statistics...")
    football_stats_raw = parse_football_stats(text)

    # Save raw stats
    with open('/home/user/frederick_sports/football_stats_raw.json', 'w') as f:
        json.dump(football_stats_raw, f, indent=2)

    # Structure the stats
    print("\nStructuring data...")
    football_stats = structure_stats(football_stats_raw)

    # Save structured stats
    with open('/home/user/frederick_sports/football_stats.json', 'w') as f:
        json.dump(football_stats, f, indent=2)

    print(f"\nFootball stats parsed:")
    print(f"  Rushing leaders: {len(football_stats['rushing'])} entries")
    print(f"  Passing leaders: {len(football_stats['passing'])} entries")
    print(f"  Receiving leaders: {len(football_stats['receiving'])} entries")

    # Show sample data
    if football_stats['rushing']:
        print("\nSample rushing leader:")
        leader = football_stats['rushing'][0]
        print(f"  {leader.get('player', 'N/A')}, {leader.get('school', 'N/A')}")
        print(f"  {leader.get('att', 'N/A')} Att, {leader.get('yds', 'N/A')} Yds, {leader.get('avg', 'N/A')} Avg, {leader.get('td', 'N/A')} TD")

    print("\nStats saved to football_stats.json")

    # Generate HTML
    print("\nGenerating HTML page...")
    html = generate_html(football_stats, "Football")

    # Save HTML to both hs_hangout and docs directories
    html_filename = 'player_stats_football_2025_10_23.html'
    output_path_hs = f'/home/user/frederick_sports/hs_hangout/{html_filename}'
    output_path_docs = f'/home/user/frederick_sports/docs/{html_filename}'

    with open(output_path_hs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_hs}")

    with open(output_path_docs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_docs}")

    print("\n✓ Football player stats extraction and HTML generation complete!")


if __name__ == '__main__':
    main()
