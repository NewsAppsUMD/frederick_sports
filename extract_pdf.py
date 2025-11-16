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


def parse_football_stats(text: str, section_index: int = -1, sport_name: str = "Football") -> Dict[str, List[Dict[str, Any]]]:
    """
    Parse football player statistics from extracted text.

    Args:
        text: Extracted PDF text
        section_index: Which INDIVIDUAL LEADERS section to use (0=first, -1=last)
        sport_name: Name of sport for debug output

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
    individual_leaders_indices = []
    for i, line in enumerate(lines):
        if line.strip() == 'INDIVIDUAL LEADERS':
            individual_leaders_indices.append(i)

    if not individual_leaders_indices:
        print(f"DEBUG: No INDIVIDUAL LEADERS sections found")
        return stats

    # Use the specified INDIVIDUAL LEADERS section
    if abs(section_index) > len(individual_leaders_indices):
        print(f"ERROR: Section index {section_index} out of range (found {len(individual_leaders_indices)} sections)")
        return stats

    start_idx = individual_leaders_indices[section_index]
    print(f"DEBUG [{sport_name}]: Found {len(individual_leaders_indices)} INDIVIDUAL LEADERS sections")
    print(f"DEBUG [{sport_name}]: Using section {section_index} at line {start_idx}")

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
            print(f"DEBUG [{sport_name}]: Found RUSHING section at line {i}")
            continue
        elif stripped == 'PASSING':
            save_current_player()
            current_section = 'passing'
            print(f"DEBUG [{sport_name}]: Found PASSING section at line {i}")
            continue
        elif stripped == 'RECEIVING':
            save_current_player()
            current_section = 'receiving'
            print(f"DEBUG [{sport_name}]: Found RECEIVING section at line {i}")
            continue

        # Stop conditions
        # 1. Empty line followed by non-data (end of stats)
        if current_section == 'receiving' and stripped == '':
            # Check if we've hit the end
            if i + 1 < len(lines) and lines[i+1].strip() == '':
                save_current_player()
                break

        # 2. Stop if we hit a new sport/section indicator
        if current_section and any(keyword in stripped for keyword in [
            '9-hole Average',  # Golf section
            'FCPS',  # New standings section
            'CENTRAL MARYLAND',  # New conference section
            'OTHER SCHOOLS',  # Separate section (might appear in some sports)
        ]):
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

            # Check if this is a new player entry (contains comma in "Name, School" format)
            # Player lines have format: "Player Name, School"
            # Stats lines might have commas in numbers like "2,150"
            # A player line has a comma followed by a space and then a word (school name)
            is_player_line = False
            if ',' in stripped:
                # Check if comma is followed by a space and text (indicating "Name, School")
                comma_idx = stripped.find(',')
                if comma_idx > 0 and comma_idx < len(stripped) - 1:
                    # Check what comes after the comma
                    after_comma = stripped[comma_idx + 1:].strip()
                    # If it starts with a letter (school name), it's a player line
                    if after_comma and after_comma[0].isalpha():
                        is_player_line = True

            if is_player_line:
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


def parse_soccer_stats(text: str, sport_name: str = "Boys Soccer") -> Dict[str, List[Dict[str, Any]]]:
    """
    Parse soccer player statistics from extracted text.

    Args:
        text: Extracted PDF text
        sport_name: Name of sport for debug output

    Returns dict with keys: scoring, goalkeepers
    """
    stats = {
        'scoring': [],
        'goalkeepers': []
    }

    # Split text into lines for easier parsing
    lines = text.split('\n')

    # Find SCORING LEADERS sections by looking for the sport's conference structure
    # Boys Soccer comes before Girls Soccer
    scoring_indices = []
    goalkeeper_indices = []

    for i, line in enumerate(lines):
        if line.strip() == 'SCORING LEADERS':
            scoring_indices.append(i)
        if line.strip() == 'GOALKEEPER STATISTICS':
            goalkeeper_indices.append(i)

    print(f"DEBUG [{sport_name}]: Found {len(scoring_indices)} SCORING LEADERS sections")
    print(f"DEBUG [{sport_name}]: Found {len(goalkeeper_indices)} GOALKEEPER STATISTICS sections")

    # Determine which sections to use based on sport
    if "Boys" in sport_name:
        # Boys Soccer is first
        scoring_idx = scoring_indices[0] if len(scoring_indices) > 0 else None
        # Boys Soccer goalkeeper is second (after Field Hockey)
        goalkeeper_idx = goalkeeper_indices[1] if len(goalkeeper_indices) > 1 else None
    else:  # Girls Soccer
        # Girls Soccer is second
        scoring_idx = scoring_indices[1] if len(scoring_indices) > 1 else None
        # Girls Soccer goalkeeper is third
        goalkeeper_idx = goalkeeper_indices[2] if len(goalkeeper_indices) > 2 else None

    # Parse Scoring Leaders
    if scoring_idx is not None:
        print(f"DEBUG [{sport_name}]: Parsing SCORING LEADERS at line {scoring_idx}")
        current_player_lines = []

        def save_scoring_player():
            if current_player_lines:
                combined = '\t'.join(current_player_lines)
                stats['scoring'].append({'raw': combined})
                current_player_lines.clear()

        for i in range(scoring_idx, len(lines)):
            stripped = lines[i].strip()

            # Stop conditions
            if any(keyword in stripped for keyword in ['GOALKEEPER STATISTICS', 'FCPS', 'CENTRAL MARYLAND']):
                save_scoring_player()
                break

            # Skip headers
            if 'Player, School' in stripped or 'GP' in stripped and 'Pts' in stripped:
                continue

            # Check for player line
            is_player_line = False
            if ',' in stripped:
                comma_idx = stripped.find(',')
                if comma_idx > 0 and comma_idx < len(stripped) - 1:
                    after_comma = stripped[comma_idx + 1:].strip()
                    if after_comma and after_comma[0].isalpha():
                        is_player_line = True

            if is_player_line:
                save_scoring_player()
                current_player_lines.append(stripped)
            elif current_player_lines:
                current_player_lines.append(stripped)

        save_scoring_player()

    # Parse Goalkeeper Statistics
    if goalkeeper_idx is not None:
        print(f"DEBUG [{sport_name}]: Parsing GOALKEEPER STATISTICS at line {goalkeeper_idx}")
        current_player_lines = []

        def save_goalkeeper():
            if current_player_lines:
                combined = '\t'.join(current_player_lines)
                stats['goalkeepers'].append({'raw': combined})
                current_player_lines.clear()

        for i in range(goalkeeper_idx, len(lines)):
            stripped = lines[i].strip()

            # Stop conditions
            if any(keyword in stripped for keyword in ['FCPS', 'CENTRAL MARYLAND', 'SCORING LEADERS']):
                save_goalkeeper()
                break

            # Skip headers
            if 'Player, School' in stripped or ('GP' in stripped and 'GAA' in stripped):
                continue
            if 'GA' in stripped and 'SO' in stripped:
                continue

            # Check for player line
            is_player_line = False
            if ',' in stripped:
                comma_idx = stripped.find(',')
                if comma_idx > 0 and comma_idx < len(stripped) - 1:
                    after_comma = stripped[comma_idx + 1:].strip()
                    if after_comma and after_comma[0].isalpha():
                        is_player_line = True

            if is_player_line:
                save_goalkeeper()
                current_player_lines.append(stripped)
            elif current_player_lines:
                current_player_lines.append(stripped)

        save_goalkeeper()

    return stats


def parse_volleyball_stats(text: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Parse volleyball player statistics from extracted text.

    Returns dict with keys: kills, assists, digs
    """
    stats = {
        'kills': [],
        'assists': [],
        'digs': []
    }

    # Split text into lines for easier parsing
    lines = text.split('\n')

    # Find the volleyball INDIVIDUAL LEADERS section (first one, index 0)
    individual_leaders_indices = []
    for i, line in enumerate(lines):
        if line.strip() == 'INDIVIDUAL LEADERS':
            individual_leaders_indices.append(i)

    if not individual_leaders_indices:
        print("DEBUG [Volleyball]: No INDIVIDUAL LEADERS sections found")
        return stats

    # Use the first INDIVIDUAL LEADERS section (Volleyball)
    start_idx = individual_leaders_indices[0]
    print(f"DEBUG [Volleyball]: Found {len(individual_leaders_indices)} INDIVIDUAL LEADERS sections")
    print(f"DEBUG [Volleyball]: Using first section at line {start_idx}")

    current_section = None
    current_player_lines = []

    def save_current_player():
        """Save accumulated player lines as one entry."""
        if current_player_lines:
            combined = '\t'.join(current_player_lines)
            stats[current_section].append({'raw': combined})
            current_player_lines.clear()

    for i in range(start_idx, len(lines)):
        stripped = lines[i].strip()

        # Identify section headers
        if stripped == 'KILLS':
            save_current_player()
            current_section = 'kills'
            print(f"DEBUG [Volleyball]: Found KILLS section at line {i}")
            continue
        elif stripped == 'ASSISTS':
            save_current_player()
            current_section = 'assists'
            print(f"DEBUG [Volleyball]: Found ASSISTS section at line {i}")
            continue
        elif stripped == 'DIGS':
            save_current_player()
            current_section = 'digs'
            print(f"DEBUG [Volleyball]: Found DIGS section at line {i}")
            continue

        # Stop conditions
        if current_section and any(keyword in stripped for keyword in [
            'CENTRAL MARYLAND CONFERENCE',  # Field Hockey section starts
            'FCPS',  # New standings section
        ]):
            save_current_player()
            break

        # Parse player data
        if current_section and stripped:
            # Skip column header lines
            if 'Player, School' in stripped:
                continue
            if 'SP' in stripped and ('Kills' in stripped or 'Digs' in stripped or 'Avg' in stripped):
                continue
            if 'Asts.' in stripped or 'Hit%' in stripped:
                continue

            # Check if this is a new player entry
            is_player_line = False
            if ',' in stripped:
                comma_idx = stripped.find(',')
                if comma_idx > 0 and comma_idx < len(stripped) - 1:
                    after_comma = stripped[comma_idx + 1:].strip()
                    if after_comma and after_comma[0].isalpha():
                        is_player_line = True

            if is_player_line:
                save_current_player()
                current_player_lines.append(stripped)
            elif current_player_lines:
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


def parse_soccer_player_entry(raw: str, stat_type: str) -> Dict[str, Any]:
    """
    Parse a raw soccer player entry into structured data.

    Args:
        raw: Raw text like "Player Name, School\tGP\tG\tA\tPts"
        stat_type: Type of stats ('scoring', 'goalkeepers')

    Returns:
        Dict with player name, school, and stats
    """
    if ',' not in raw:
        return None

    parts = raw.split(',', 1)
    player_name = parts[0].strip()
    rest = parts[1].strip()

    # Split rest by tabs to get school and stats
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
    if stat_type == 'scoring':
        # Scoring: GP, G, A, Pts
        if len(stats_values) >= 1:
            result['gp'] = stats_values[0]
        if len(stats_values) >= 2:
            result['g'] = stats_values[1]
        if len(stats_values) >= 3:
            result['a'] = stats_values[2]
        if len(stats_values) >= 4:
            result['pts'] = stats_values[3]
    elif stat_type == 'goalkeepers':
        # Goalkeepers: GP, GA, SO, SV%, GAA
        if len(stats_values) >= 1:
            result['gp'] = stats_values[0]
        if len(stats_values) >= 2:
            result['ga'] = stats_values[1]
        if len(stats_values) >= 3:
            result['so'] = stats_values[2]
        if len(stats_values) >= 4:
            result['sv_pct'] = stats_values[3]
        if len(stats_values) >= 5:
            result['gaa'] = stats_values[4]

    return result


def parse_volleyball_player_entry(raw: str, stat_type: str) -> Dict[str, Any]:
    """
    Parse a raw volleyball player entry into structured data.

    Args:
        raw: Raw text like "Player Name, School\tSP\tKills\tHit%\tAvg"
        stat_type: Type of stats ('kills', 'assists', 'digs')

    Returns:
        Dict with player name, school, and stats
    """
    if ',' not in raw:
        return None

    parts = raw.split(',', 1)
    player_name = parts[0].strip()
    rest = parts[1].strip()

    # Split rest by tabs to get school and stats
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
    if stat_type == 'kills':
        # Kills: SP, Kills, Hit%, Avg
        if len(stats_values) >= 1:
            result['sp'] = stats_values[0]
        if len(stats_values) >= 2:
            result['kills'] = stats_values[1]
        if len(stats_values) >= 3:
            result['hit_pct'] = stats_values[2]
        if len(stats_values) >= 4:
            result['avg'] = stats_values[3]
    elif stat_type == 'assists':
        # Assists: SP (if present), Asts, Digs, Avg
        # Note: Some entries may not have SP
        if len(stats_values) >= 1:
            result['sp'] = stats_values[0] if len(stats_values) == 4 else ''
        if len(stats_values) >= 2:
            result['asts'] = stats_values[1] if len(stats_values) == 4 else stats_values[0]
        if len(stats_values) >= 3:
            result['digs'] = stats_values[2] if len(stats_values) == 4 else stats_values[1]
        if len(stats_values) >= 3:
            result['avg'] = stats_values[3] if len(stats_values) == 4 else stats_values[2]
    elif stat_type == 'digs':
        # Digs: SP, Digs, Avg
        if len(stats_values) >= 1:
            result['sp'] = stats_values[0]
        if len(stats_values) >= 2:
            result['digs'] = stats_values[1]
        if len(stats_values) >= 3:
            result['avg'] = stats_values[2]

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


def structure_soccer_stats(raw_stats: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
    """Convert raw soccer stats to structured format."""
    structured = {
        'scoring': [],
        'goalkeepers': []
    }

    for stat_type in ['scoring', 'goalkeepers']:
        for entry in raw_stats[stat_type]:
            parsed = parse_soccer_player_entry(entry['raw'], stat_type)
            if parsed:
                structured[stat_type].append(parsed)

    return structured


def structure_volleyball_stats(raw_stats: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
    """Convert raw volleyball stats to structured format."""
    structured = {
        'kills': [],
        'assists': [],
        'digs': []
    }

    for stat_type in ['kills', 'assists', 'digs']:
        for entry in raw_stats[stat_type]:
            parsed = parse_volleyball_player_entry(entry['raw'], stat_type)
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


def generate_soccer_html(stats: Dict[str, List[Dict]], sport: str = "Boys Soccer") -> str:
    """Generate HTML page for soccer player stats."""

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

    # Scoring Leaders
    if stats.get('scoring'):
        html += """
            <div class="sport-section">
                <h2 class="section-title">Scoring Leaders</h2>
                <table class="stats-table">
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>School</th>
                            <th>GP</th>
                            <th>G</th>
                            <th>A</th>
                            <th>Pts</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for player in stats['scoring']:
            html += f"""                        <tr>
                            <td>{player.get('player', '')}</td>
                            <td>{player.get('school', '')}</td>
                            <td>{player.get('gp', '')}</td>
                            <td>{player.get('g', '')}</td>
                            <td>{player.get('a', '')}</td>
                            <td>{player.get('pts', '')}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
            </div>
"""

    # Goalkeeper Statistics
    if stats.get('goalkeepers'):
        html += """
            <div class="sport-section">
                <h2 class="section-title">Goalkeeper Statistics</h2>
                <table class="stats-table">
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>School</th>
                            <th>GP</th>
                            <th>GA</th>
                            <th>SO</th>
                            <th>SV%</th>
                            <th>GAA</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for player in stats['goalkeepers']:
            html += f"""                        <tr>
                            <td>{player.get('player', '')}</td>
                            <td>{player.get('school', '')}</td>
                            <td>{player.get('gp', '')}</td>
                            <td>{player.get('ga', '')}</td>
                            <td>{player.get('so', '')}</td>
                            <td>{player.get('sv_pct', '')}</td>
                            <td>{player.get('gaa', '')}</td>
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
            <p>GP = Games Played, G = Goals, A = Assists, Pts = Points, GA = Goals Against, SO = Shutouts, SV% = Save Percentage, GAA = Goals Against Average</p>
            <p><strong>Data Source:</strong> The Frederick News-Post - High School Hangout</p>
            <p>Statistics submitted by coaches and team statisticians</p>
        </footer>
    </div>
</body>
</html>
"""

    return html


def generate_volleyball_html(stats: Dict[str, List[Dict]], sport: str = "Volleyball") -> str:
    """Generate HTML page for volleyball player stats."""

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

    # Kills Leaders
    if stats.get('kills'):
        html += """
            <div class="sport-section">
                <h2 class="section-title">Kills Leaders</h2>
                <table class="stats-table">
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>School</th>
                            <th>SP</th>
                            <th>Kills</th>
                            <th>Hit%</th>
                            <th>Avg</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for player in stats['kills']:
            html += f"""                        <tr>
                            <td>{player.get('player', '')}</td>
                            <td>{player.get('school', '')}</td>
                            <td>{player.get('sp', '')}</td>
                            <td>{player.get('kills', '')}</td>
                            <td>{player.get('hit_pct', '')}</td>
                            <td>{player.get('avg', '')}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
            </div>
"""

    # Assists Leaders
    if stats.get('assists'):
        html += """
            <div class="sport-section">
                <h2 class="section-title">Assists Leaders</h2>
                <table class="stats-table">
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>School</th>
                            <th>SP</th>
                            <th>Asts</th>
                            <th>Digs</th>
                            <th>Avg</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for player in stats['assists']:
            html += f"""                        <tr>
                            <td>{player.get('player', '')}</td>
                            <td>{player.get('school', '')}</td>
                            <td>{player.get('sp', '')}</td>
                            <td>{player.get('asts', '')}</td>
                            <td>{player.get('digs', '')}</td>
                            <td>{player.get('avg', '')}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
            </div>
"""

    # Digs Leaders
    if stats.get('digs'):
        html += """
            <div class="sport-section">
                <h2 class="section-title">Digs Leaders</h2>
                <table class="stats-table">
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>School</th>
                            <th>SP</th>
                            <th>Digs</th>
                            <th>Avg</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for player in stats['digs']:
            html += f"""                        <tr>
                            <td>{player.get('player', '')}</td>
                            <td>{player.get('school', '')}</td>
                            <td>{player.get('sp', '')}</td>
                            <td>{player.get('digs', '')}</td>
                            <td>{player.get('avg', '')}</td>
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
            <p>SP = Sets Played, Hit% = Hitting Percentage, Avg = Average, Asts = Assists</p>
            <p><strong>Data Source:</strong> The Frederick News-Post - High School Hangout</p>
            <p>Statistics submitted by coaches and team statisticians</p>
        </footer>
    </div>
</body>
</html>
"""

    return html


def process_sport(text: str, sport_name: str, section_index: int, file_prefix: str):
    """Process a single sport's stats."""
    print(f"\n{'='*60}")
    print(f"Processing {sport_name}")
    print(f"{'='*60}")

    # Parse stats
    print(f"\nParsing {sport_name} statistics...")
    stats_raw = parse_football_stats(text, section_index=section_index, sport_name=sport_name)

    # Save raw stats
    raw_filename = f'{file_prefix}_stats_raw.json'
    with open(f'/home/user/frederick_sports/{raw_filename}', 'w') as f:
        json.dump(stats_raw, f, indent=2)

    # Structure the stats
    print(f"\nStructuring data...")
    stats = structure_stats(stats_raw)

    # Save structured stats
    stats_filename = f'{file_prefix}_stats.json'
    with open(f'/home/user/frederick_sports/{stats_filename}', 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\n{sport_name} stats parsed:")
    print(f"  Rushing leaders: {len(stats['rushing'])} entries")
    print(f"  Passing leaders: {len(stats['passing'])} entries")
    print(f"  Receiving leaders: {len(stats['receiving'])} entries")

    # Show sample data
    if stats['rushing']:
        print(f"\nSample rushing leader:")
        leader = stats['rushing'][0]
        print(f"  {leader.get('player', 'N/A')}, {leader.get('school', 'N/A')}")
        print(f"  {leader.get('att', 'N/A')} Att, {leader.get('yds', 'N/A')} Yds, {leader.get('avg', 'N/A')} Avg, {leader.get('td', 'N/A')} TD")

    print(f"\nStats saved to {stats_filename}")

    # Generate HTML
    print(f"\nGenerating HTML page...")
    html = generate_html(stats, sport_name)

    # Save HTML to both hs_hangout and docs directories
    html_filename = f'player_stats_{file_prefix}_2025_10_23.html'
    output_path_hs = f'/home/user/frederick_sports/hs_hangout/{html_filename}'
    output_path_docs = f'/home/user/frederick_sports/docs/{html_filename}'

    with open(output_path_hs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_hs}")

    with open(output_path_docs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_docs}")

    print(f"\n✓ {sport_name} player stats extraction and HTML generation complete!")


def process_soccer_sport(text: str, sport_name: str, file_prefix: str):
    """Process a soccer sport's stats."""
    print(f"\n{'='*60}")
    print(f"Processing {sport_name}")
    print(f"{'='*60}")

    # Parse stats
    print(f"\nParsing {sport_name} statistics...")
    stats_raw = parse_soccer_stats(text, sport_name=sport_name)

    # Save raw stats
    raw_filename = f'{file_prefix}_stats_raw.json'
    with open(f'/home/user/frederick_sports/{raw_filename}', 'w') as f:
        json.dump(stats_raw, f, indent=2)

    # Structure the stats
    print(f"\nStructuring data...")
    stats = structure_soccer_stats(stats_raw)

    # Save structured stats
    stats_filename = f'{file_prefix}_stats.json'
    with open(f'/home/user/frederick_sports/{stats_filename}', 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\n{sport_name} stats parsed:")
    print(f"  Scoring leaders: {len(stats['scoring'])} entries")
    print(f"  Goalkeepers: {len(stats['goalkeepers'])} entries")

    # Show sample data
    if stats['scoring']:
        print(f"\nSample scoring leader:")
        leader = stats['scoring'][0]
        print(f"  {leader.get('player', 'N/A')}, {leader.get('school', 'N/A')}")
        print(f"  {leader.get('gp', 'N/A')} GP, {leader.get('g', 'N/A')} G, {leader.get('a', 'N/A')} A, {leader.get('pts', 'N/A')} Pts")

    print(f"\nStats saved to {stats_filename}")

    # Generate HTML
    print(f"\nGenerating HTML page...")
    html = generate_soccer_html(stats, sport_name)

    # Save HTML to both hs_hangout and docs directories
    html_filename = f'player_stats_{file_prefix}_2025_10_23.html'
    output_path_hs = f'/home/user/frederick_sports/hs_hangout/{html_filename}'
    output_path_docs = f'/home/user/frederick_sports/docs/{html_filename}'

    with open(output_path_hs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_hs}")

    with open(output_path_docs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_docs}")

    print(f"\n✓ {sport_name} player stats extraction and HTML generation complete!")


def process_volleyball_sport(text: str):
    """Process volleyball stats."""
    sport_name = "Volleyball"
    file_prefix = "volleyball"

    print(f"\n{'='*60}")
    print(f"Processing {sport_name}")
    print(f"{'='*60}")

    # Parse stats
    print(f"\nParsing {sport_name} statistics...")
    stats_raw = parse_volleyball_stats(text)

    # Save raw stats
    raw_filename = f'{file_prefix}_stats_raw.json'
    with open(f'/home/user/frederick_sports/{raw_filename}', 'w') as f:
        json.dump(stats_raw, f, indent=2)

    # Structure the stats
    print(f"\nStructuring data...")
    stats = structure_volleyball_stats(stats_raw)

    # Save structured stats
    stats_filename = f'{file_prefix}_stats.json'
    with open(f'/home/user/frederick_sports/{stats_filename}', 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\n{sport_name} stats parsed:")
    print(f"  Kills leaders: {len(stats['kills'])} entries")
    print(f"  Assists leaders: {len(stats['assists'])} entries")
    print(f"  Digs leaders: {len(stats['digs'])} entries")

    # Show sample data
    if stats['kills']:
        print(f"\nSample kills leader:")
        leader = stats['kills'][0]
        print(f"  {leader.get('player', 'N/A')}, {leader.get('school', 'N/A')}")
        print(f"  {leader.get('sp', 'N/A')} SP, {leader.get('kills', 'N/A')} Kills, {leader.get('avg', 'N/A')} Avg")

    print(f"\nStats saved to {stats_filename}")

    # Generate HTML
    print(f"\nGenerating HTML page...")
    html = generate_volleyball_html(stats, sport_name)

    # Save HTML to both hs_hangout and docs directories
    html_filename = f'player_stats_{file_prefix}_2025_10_23.html'
    output_path_hs = f'/home/user/frederick_sports/hs_hangout/{html_filename}'
    output_path_docs = f'/home/user/frederick_sports/docs/{html_filename}'

    with open(output_path_hs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_hs}")

    with open(output_path_docs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_docs}")

    print(f"\n✓ {sport_name} player stats extraction and HTML generation complete!")


def main():
    """Main extraction function."""
    pdf_path = '/home/user/frederick_sports/hs_hangout/2025_10_23.pdf'

    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)

    # Save full text for inspection
    with open('/home/user/frederick_sports/pdf_text.txt', 'w') as f:
        f.write(text)
    print(f"Full text saved to pdf_text.txt ({len(text)} characters)")

    # Process football sports (rushing/passing/receiving)
    football_sports = [
        ("Girls Flag Football", 0, "girls_flag_football"),
        ("Football", -1, "football"),
    ]

    for sport_name, section_index, file_prefix in football_sports:
        process_sport(text, sport_name, section_index, file_prefix)

    # Process soccer sports (scoring/goalkeepers)
    soccer_sports = [
        ("Boys Soccer", "boys_soccer"),
        ("Girls Soccer", "girls_soccer"),
    ]

    for sport_name, file_prefix in soccer_sports:
        process_soccer_sport(text, sport_name, file_prefix)

    # Process volleyball
    process_volleyball_sport(text)

    print(f"\n{'='*60}")
    print("ALL SPORTS COMPLETE!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
