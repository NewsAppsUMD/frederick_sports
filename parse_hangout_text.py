#!/usr/bin/env python3
"""
Parse the FNP High School Hangout semicolon-delimited text file
and generate an HTML page for winter sports stats.

Usage:
    python parse_hangout_text.py
"""

import html
import json
import os
import re


def read_file(filepath):
    """Read the text file and return non-empty lines."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()
    # Split into lines, strip whitespace, keep non-empty
    lines = [line.strip() for line in raw.split('\n')]
    return lines


def parse_hangout_text(filepath):
    """Parse the semicolon-delimited hangout text file into structured data."""
    lines = read_file(filepath)

    # Remove empty lines for easier processing, but track structure
    # We'll process line by line with empty-line awareness
    data = {
        'boys_basketball': {'standings': {}, 'leaders': {}},
        'girls_basketball': {'standings': {}, 'leaders': {}},
        'boys_wrestling': {'weight_classes': []},
        'girls_wrestling': {'weight_classes': []},
        'indoor_track': {'boys': {}, 'girls': {}},
        'swimming': {'boys': {}, 'girls': {}},
        'rankings': {}
    }

    # Find major section boundaries
    i = 0
    sections = []
    current_section_start = None
    current_section_name = None

    # Identify top-level sport sections
    major_sports = [
        'Boys Basketball', 'Girls Basketball',
        'Boys Wrestling', 'Girls Wrestling',
        'Indoor Track and Field', 'Swimming & Diving',
        'Rankings'
    ]

    section_indices = {}
    for idx, line in enumerate(lines):
        stripped = line.strip()
        for sport in major_sports:
            if stripped == sport and sport not in section_indices:
                section_indices[sport] = idx
                break

    # Parse each section
    if 'Boys Basketball' in section_indices:
        end = section_indices.get('Girls Basketball', len(lines))
        data['boys_basketball'] = parse_basketball_section(lines[section_indices['Boys Basketball']:end])

    if 'Girls Basketball' in section_indices:
        end = section_indices.get('Boys Wrestling', len(lines))
        data['girls_basketball'] = parse_basketball_section(lines[section_indices['Girls Basketball']:end])

    if 'Boys Wrestling' in section_indices:
        end = section_indices.get('Girls Wrestling', len(lines))
        data['boys_wrestling'] = parse_wrestling_section(lines[section_indices['Boys Wrestling']:end])

    if 'Girls Wrestling' in section_indices:
        end = section_indices.get('Indoor Track and Field', len(lines))
        data['girls_wrestling'] = parse_wrestling_section(lines[section_indices['Girls Wrestling']:end])

    if 'Indoor Track and Field' in section_indices:
        end = section_indices.get('Swimming & Diving', len(lines))
        data['indoor_track'] = parse_track_section(lines[section_indices['Indoor Track and Field']:end])

    if 'Swimming & Diving' in section_indices:
        end = section_indices.get('Rankings', len(lines))
        data['swimming'] = parse_swimming_section(lines[section_indices['Swimming & Diving']:end])

    if 'Rankings' in section_indices:
        data['rankings'] = parse_rankings_section(lines[section_indices['Rankings']:])

    return data


def parse_basketball_section(lines):
    """Parse a basketball section (boys or girls) with standings and individual leaders."""
    result = {'standings': {}, 'leaders': {}}

    # Find sub-sections
    i = 0
    # Skip the sport title line
    while i < len(lines) and lines[i].strip() in ('', 'Boys Basketball', 'Girls Basketball'):
        i += 1

    # Parse standings divisions
    division_names = ['Spires Division', 'Potomac Division', 'Gambrill Division', 'Antietam Division']
    current_division = None
    in_other_schools = False
    in_leaders = False
    current_leader_category = None

    while i < len(lines):
        line = lines[i].strip()

        if line == '':
            i += 1
            continue

        # Check for Individual Leaders section
        if line == 'Individual Leaders':
            in_leaders = True
            i += 1
            continue

        if in_leaders:
            # Check for leader categories
            if line in ('Scoring', 'Rebounds', 'Rebounding', 'Assists'):
                current_leader_category = line.lower()
                if current_leader_category == 'rebounding':
                    current_leader_category = 'rebounds'
                i += 1
                # Skip the header line if present (some sections lack it)
                while i < len(lines):
                    hline = lines[i].strip()
                    if hline == '':
                        i += 1
                        continue
                    if hline.startswith('Player'):
                        i += 1
                        break
                    # If we hit a data line (has ; and comma), stop skipping
                    if ';' in hline and ',' in hline:
                        break
                    i += 1
                # Parse player entries
                result['leaders'][current_leader_category] = []
                while i < len(lines):
                    pline = lines[i].strip()
                    if pline == '':
                        i += 1
                        continue
                    # Check if we've hit a new category or end
                    if pline in ('Scoring', 'Rebounds', 'Rebounding', 'Assists',
                                 'Girls Basketball', 'Boys Wrestling', 'Girls Wrestling',
                                 'Indoor Track and Field', 'Swimming & Diving', 'Rankings'):
                        break
                    # Parse player line: "Player, School;GP;Stat;Avg."
                    parts = pline.split(';')
                    if len(parts) >= 3 and ',' in parts[0]:
                        player_school = parts[0].strip()
                        # Split on last comma to get player and school
                        comma_idx = player_school.rfind(',')
                        player = player_school[:comma_idx].strip()
                        school = player_school[comma_idx+1:].strip()
                        entry = {
                            'player': player,
                            'school': school,
                            'values': [p.strip() for p in parts[1:]]
                        }
                        result['leaders'][current_leader_category].append(entry)
                    i += 1
                continue
            else:
                i += 1
                continue

        # Check for division headers
        matched_division = False
        for div_name in division_names:
            if line == div_name:
                current_division = div_name
                in_other_schools = False
                result['standings'][current_division] = []
                i += 1
                # Skip header lines
                while i < len(lines):
                    hline = lines[i].strip()
                    if hline == '' or hline.startswith(';') or hline.startswith('School'):
                        i += 1
                        continue
                    break
                matched_division = True
                break

        if matched_division:
            # Parse team rows for this division
            while i < len(lines):
                tline = lines[i].strip()
                if tline == '':
                    i += 1
                    continue
                # Check if we've hit a new section
                if tline in division_names or tline == 'Other Schools' or tline == 'Individual Leaders':
                    break
                # Parse team: "School;W;L;;W;L" or "School;W;L;W;L"
                parts = tline.split(';')
                team_name = parts[0].strip()
                if team_name and not team_name.startswith(';'):
                    # Filter out empty parts and get numbers
                    nums = [p.strip() for p in parts[1:] if p.strip() != '']
                    if len(nums) >= 4:
                        result['standings'][current_division].append({
                            'team': team_name,
                            'div_w': nums[0], 'div_l': nums[1],
                            'overall_w': nums[2], 'overall_l': nums[3]
                        })
                    elif len(nums) >= 2:
                        result['standings'][current_division].append({
                            'team': team_name,
                            'div_w': nums[0], 'div_l': nums[1],
                            'overall_w': '', 'overall_l': ''
                        })
                i += 1
            continue

        # Check for Other Schools
        if line == 'Other Schools':
            in_other_schools = True
            result['standings']['Other Schools'] = []
            i += 1
            # Skip header lines
            while i < len(lines):
                hline = lines[i].strip()
                if hline == '' or hline.startswith(';') or hline.startswith('Team'):
                    i += 1
                    continue
                break
            # Parse team rows
            while i < len(lines):
                tline = lines[i].strip()
                if tline == '':
                    i += 1
                    continue
                if tline == 'Individual Leaders':
                    break
                parts = tline.split(';')
                team_name = parts[0].strip()
                if team_name:
                    nums = [p.strip() for p in parts[1:] if p.strip() != '']
                    if len(nums) >= 2:
                        result['standings']['Other Schools'].append({
                            'team': team_name,
                            'w': nums[0], 'l': nums[1]
                        })
                i += 1
            continue

        # Check for "Central Maryland Conference" header - skip it
        if line == 'Central Maryland Conference':
            i += 1
            continue

        i += 1

    return result


def parse_wrestling_section(lines):
    """Parse a wrestling section with weight class rankings."""
    result = {'weight_classes': []}

    i = 0
    # Skip header
    while i < len(lines) and lines[i].strip() in ('', 'Boys Wrestling', 'Girls Wrestling', 'Teams'):
        i += 1

    current_weight = None
    while i < len(lines):
        line = lines[i].strip()
        if line == '':
            i += 1
            continue

        # Check for end of section
        if line in ('Girls Wrestling', 'Indoor Track and Field', 'Swimming & Diving', 'Rankings'):
            break

        # Check if this is a weight class (number only)
        if re.match(r'^\d+$', line):
            current_weight = line
            result['weight_classes'].append({
                'weight': current_weight,
                'wrestlers': []
            })
            i += 1
            continue

        # Check for ranked wrestler: "1. Name, School"
        match = re.match(r'^(\d+)\.\s+(.+),\s+(.+)$', line)
        if match and current_weight:
            rank = match.group(1)
            name = match.group(2).strip()
            school = match.group(3).strip()
            result['weight_classes'][-1]['wrestlers'].append({
                'rank': rank,
                'name': name,
                'school': school
            })
            i += 1
            continue

        i += 1

    return result


def parse_track_section(lines):
    """Parse indoor track and field section."""
    result = {'boys': {}, 'girls': {}}

    i = 0
    # Skip header
    while i < len(lines) and lines[i].strip() in ('', 'Indoor Track and Field'):
        i += 1

    current_gender = None
    current_event = None

    while i < len(lines):
        line = lines[i].strip()
        if line == '':
            i += 1
            continue

        # Check for end of section
        if line in ('Swimming & Diving', 'Rankings'):
            break

        # Check for gender headers
        if line == 'Boys':
            current_gender = 'boys'
            i += 1
            continue
        if line == 'Girls':
            current_gender = 'girls'
            i += 1
            continue

        if current_gender is None:
            i += 1
            continue

        # Check if this is an event name
        # Known event name patterns: "55-meter dash", "1,600 meters", "4x200 relay",
        # "Shot put", "High jump", "Pole vault"
        # vs athlete lines: "Name, School, Time"
        is_event = False
        # Event names with numeric distances like "1,600 meters", "3,200 meters"
        if re.match(r'^\d[\d,]+ meters$', line):
            is_event = True
        # Non-comma event names
        elif ',' not in line and not re.match(r'^\d+\.', line):
            is_event = True

        if is_event:
            current_event = line
            if current_event not in result[current_gender]:
                result[current_gender][current_event] = []
            i += 1
            continue

        # Parse athlete entry: "Name, School, Result"
        # Or relay: "Name1, Name2, ..., School, Result"
        if current_event and current_gender:
            # Split on last comma to get result
            parts = line.rsplit(',', 1)
            if len(parts) == 2:
                names_school = parts[0].strip()
                time_result = parts[1].strip()
                result[current_gender][current_event].append({
                    'entry': names_school,
                    'result': time_result
                })

        i += 1

    return result


def parse_swimming_section(lines):
    """Parse swimming & diving section."""
    result = {'boys': {}, 'girls': {}}

    i = 0
    # Skip header
    while i < len(lines) and lines[i].strip() in ('', 'Swimming & Diving'):
        i += 1

    current_gender = None
    current_event = None

    while i < len(lines):
        line = lines[i].strip()
        if line == '':
            i += 1
            continue

        # Check for end of section
        if line == 'Rankings':
            break

        # Check for gender headers
        if line in ('BOYS', 'Boys'):
            current_gender = 'boys'
            i += 1
            continue
        if line in ('GIRLS', 'Girls'):
            current_gender = 'girls'
            i += 1
            continue

        if current_gender is None:
            i += 1
            continue

        # Check if this is an event name
        # Events don't contain the athlete pattern "Name, School, Time"
        # Swimming events: "50 freestyle", "100 backstroke", etc.
        # Also relay events: "200 medley relay", "400 freestyle relay"
        # A tricky case: "Charlotte Deigan, Linganore;26.43" uses ; instead of ,
        if not re.search(r',\s*\d', line) and not re.search(r',\s*[A-Z].*,', line) and ';' not in line:
            if not re.match(r'^\d+\.', line):
                current_event = line
                if current_event not in result[current_gender]:
                    result[current_gender][current_event] = []
                i += 1
                continue

        # Parse athlete entry
        if current_event and current_gender:
            # Handle both comma and semicolon delimited entries
            # Some entries use ; as separator: "Charlotte Deigan, Linganore;26.43"
            # Normalize by replacing ; with , for consistent parsing
            normalized = line.replace(';', ',')
            parts = normalized.rsplit(',', 1)
            if len(parts) == 2:
                names_school = parts[0].strip()
                time_result = parts[1].strip()
                result[current_gender][current_event].append({
                    'entry': names_school,
                    'result': time_result
                })

        i += 1

    return result


def parse_rankings_section(lines):
    """Parse the power rankings section."""
    result = {}

    i = 0
    # Skip header
    while i < len(lines) and lines[i].strip() in ('', 'Rankings'):
        i += 1

    current_sport = None

    while i < len(lines):
        line = lines[i].strip()
        if line == '':
            i += 1
            continue

        # Check if this is a sport name (not a numbered ranking)
        if not re.match(r'^\d+\.', line):
            current_sport = line
            result[current_sport] = []
            i += 1
            continue

        # Parse ranked team: "1. Team"
        match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if match and current_sport:
            result[current_sport].append({
                'rank': match.group(1),
                'team': match.group(2).strip()
            })

        i += 1

    return result


def esc(text):
    """HTML-escape text."""
    return html.escape(str(text))


def generate_html(data, date_str=None):
    """Generate the full HTML page from parsed data."""

    # Format date for display
    if date_str:
        from datetime import datetime
        try:
            dt = datetime.strptime(date_str, '%Y_%m_%d')
            display_date = dt.strftime('%B %d, %Y').replace(' 0', ' ')
        except ValueError:
            display_date = date_str
    else:
        display_date = 'January 29, 2026'

    html_parts = []

    # HTML header with CSS (matching existing site style)
    html_parts.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Winter Sports Stats - High School Hangout ({display_date})</title>
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

        /* Table of contents / navigation */
        .toc {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px 30px;
            margin-bottom: 40px;
        }}

        .toc h3 {{
            font-size: 18px;
            color: #333;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .toc ul {{
            list-style: none;
            padding: 0;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .toc a {{
            display: inline-block;
            padding: 6px 14px;
            background-color: #333;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 14px;
            transition: background-color 0.2s ease;
        }}

        .toc a:hover {{
            background-color: #555;
        }}

        .sport-header {{
            font-size: 28px;
            color: #fff;
            background-color: #333;
            padding: 12px 20px;
            margin: 50px 0 20px 0;
            border-radius: 4px;
        }}

        .sport-section {{
            margin: 30px 0;
        }}

        .section-title {{
            font-size: 22px;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #666;
            text-transform: uppercase;
        }}

        .subsection-title {{
            font-size: 18px;
            color: #555;
            margin: 20px 0 10px 0;
            padding-bottom: 5px;
            border-bottom: 1px solid #ccc;
        }}

        .stats-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0 30px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .stats-table th,
        .stats-table td {{
            padding: 10px 12px;
            border: 1px solid #ddd;
        }}

        .stats-table thead th {{
            background-color: #333;
            color: white;
            font-weight: bold;
            text-align: center;
            text-transform: uppercase;
            font-size: 13px;
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

        .rank {{
            color: #666;
            font-weight: bold;
            text-align: center !important;
        }}

        .weight-class {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
            background-color: #e9ecef;
            padding: 6px 12px;
            margin: 15px 0 5px 0;
            border-radius: 4px;
            display: inline-block;
        }}

        .rankings-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}

        .ranking-card {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px 20px;
        }}

        .ranking-card h4 {{
            font-size: 16px;
            color: #333;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 2px solid #333;
            text-transform: uppercase;
        }}

        .ranking-card ol {{
            padding-left: 25px;
            margin: 0;
        }}

        .ranking-card li {{
            padding: 3px 0;
            font-size: 14px;
            color: #444;
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
                padding: 15px;
            }}

            h1 {{
                font-size: 24px;
            }}

            .sport-header {{
                font-size: 22px;
            }}

            .section-title {{
                font-size: 18px;
            }}

            .stats-table th,
            .stats-table td {{
                padding: 6px 8px;
                font-size: 13px;
            }}

            .toc ul {{
                flex-direction: column;
            }}

            .rankings-grid {{
                grid-template-columns: 1fr;
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
            <h1>Frederick County Winter Sports Stats</h1>
            <p class="subtitle">Updated Through {display_date}</p>
            <p class="subtitle">Source: The Frederick News-Post High School Hangout</p>
        </header>

        <nav class="toc">
            <h3>Jump to Sport</h3>
            <ul>
                <li><a href="#boys-basketball">Boys Basketball</a></li>
                <li><a href="#girls-basketball">Girls Basketball</a></li>
                <li><a href="#boys-wrestling">Boys Wrestling</a></li>
                <li><a href="#girls-wrestling">Girls Wrestling</a></li>
                <li><a href="#indoor-track">Indoor Track &amp; Field</a></li>
                <li><a href="#swimming">Swimming &amp; Diving</a></li>
                <li><a href="#rankings">Power Rankings</a></li>
            </ul>
        </nav>

        <main>
''')

    # Boys Basketball
    html_parts.append(generate_basketball_html(data['boys_basketball'], 'Boys Basketball', 'boys-basketball'))

    # Girls Basketball
    html_parts.append(generate_basketball_html(data['girls_basketball'], 'Girls Basketball', 'girls-basketball'))

    # Boys Wrestling
    html_parts.append(generate_wrestling_html(data['boys_wrestling'], 'Boys Wrestling', 'boys-wrestling'))

    # Girls Wrestling
    html_parts.append(generate_wrestling_html(data['girls_wrestling'], 'Girls Wrestling', 'girls-wrestling'))

    # Indoor Track
    html_parts.append(generate_track_html(data['indoor_track'], 'Indoor Track & Field', 'indoor-track'))

    # Swimming
    html_parts.append(generate_swimming_html(data['swimming'], 'Swimming & Diving', 'swimming'))

    # Rankings
    html_parts.append(generate_rankings_html(data['rankings']))

    # Footer
    html_parts.append('''
        </main>

        <footer>
            <p><strong>Column Abbreviations:</strong></p>
            <p>GP = Games Played, Pts = Points, Avg = Average, Reb = Rebounds, W = Wins, L = Losses</p>
            <p><strong>Data Source:</strong> The Frederick News-Post - High School Hangout</p>
            <p>Statistics submitted by coaches and team statisticians</p>
        </footer>
    </div>
</body>
</html>
''')

    return ''.join(html_parts)


def generate_basketball_html(bball_data, title, anchor_id):
    """Generate HTML for a basketball section."""
    parts = []

    parts.append(f'\n            <h2 class="sport-header" id="{anchor_id}">{esc(title)}</h2>\n')

    # Standings
    standings = bball_data.get('standings', {})
    division_order = ['Spires Division', 'Potomac Division', 'Gambrill Division', 'Antietam Division', 'Other Schools']

    for div_name in division_order:
        if div_name not in standings or not standings[div_name]:
            continue

        teams = standings[div_name]
        parts.append(f'            <div class="sport-section">\n')
        parts.append(f'                <h3 class="section-title">{esc(div_name)}</h3>\n')

        if div_name == 'Other Schools':
            parts.append('                <table class="stats-table">\n')
            parts.append('                    <thead>\n')
            parts.append('                        <tr>\n')
            parts.append('                            <th>Team</th>\n')
            parts.append('                            <th>W</th>\n')
            parts.append('                            <th>L</th>\n')
            parts.append('                        </tr>\n')
            parts.append('                    </thead>\n')
            parts.append('                    <tbody>\n')
            for team in teams:
                parts.append('                        <tr>\n')
                parts.append(f'                            <td>{esc(team["team"])}</td>\n')
                parts.append(f'                            <td>{esc(team.get("w", ""))}</td>\n')
                parts.append(f'                            <td>{esc(team.get("l", ""))}</td>\n')
                parts.append('                        </tr>\n')
            parts.append('                    </tbody>\n')
            parts.append('                </table>\n')
        else:
            parts.append('                <table class="stats-table">\n')
            parts.append('                    <thead>\n')
            parts.append('                        <tr>\n')
            parts.append('                            <th>Team</th>\n')
            parts.append('                            <th colspan="2">Division</th>\n')
            parts.append('                            <th colspan="2">Overall</th>\n')
            parts.append('                        </tr>\n')
            parts.append('                        <tr>\n')
            parts.append('                            <th></th>\n')
            parts.append('                            <th>W</th>\n')
            parts.append('                            <th>L</th>\n')
            parts.append('                            <th>W</th>\n')
            parts.append('                            <th>L</th>\n')
            parts.append('                        </tr>\n')
            parts.append('                    </thead>\n')
            parts.append('                    <tbody>\n')
            for team in teams:
                parts.append('                        <tr>\n')
                parts.append(f'                            <td>{esc(team["team"])}</td>\n')
                parts.append(f'                            <td>{esc(team["div_w"])}</td>\n')
                parts.append(f'                            <td>{esc(team["div_l"])}</td>\n')
                parts.append(f'                            <td>{esc(team["overall_w"])}</td>\n')
                parts.append(f'                            <td>{esc(team["overall_l"])}</td>\n')
                parts.append('                        </tr>\n')
            parts.append('                    </tbody>\n')
            parts.append('                </table>\n')

        parts.append('            </div>\n')

    # Individual Leaders
    leaders = bball_data.get('leaders', {})
    leader_configs = {
        'scoring': {'title': 'Scoring Leaders', 'headers': ['Player', 'School', 'GP', 'Pts', 'Avg']},
        'rebounds': {'title': 'Rebounding Leaders', 'headers': ['Player', 'School', 'GP', 'Reb', 'Avg']},
        'assists': {'title': 'Assists Leaders', 'headers': ['Player', 'School', 'GP', 'Ast', 'Avg']},
    }

    for cat_key in ['scoring', 'rebounds', 'assists']:
        if cat_key not in leaders or not leaders[cat_key]:
            continue

        config = leader_configs[cat_key]
        players = leaders[cat_key]

        parts.append(f'            <div class="sport-section">\n')
        parts.append(f'                <h3 class="section-title">{esc(config["title"])}</h3>\n')
        parts.append('                <table class="stats-table">\n')
        parts.append('                    <thead>\n')
        parts.append('                        <tr>\n')
        for h in config['headers']:
            parts.append(f'                            <th>{esc(h)}</th>\n')
        parts.append('                        </tr>\n')
        parts.append('                    </thead>\n')
        parts.append('                    <tbody>\n')

        for player in players:
            parts.append('                        <tr>\n')
            parts.append(f'                            <td>{esc(player["player"])}</td>\n')
            parts.append(f'                            <td>{esc(player["school"])}</td>\n')
            for val in player['values']:
                parts.append(f'                            <td>{esc(val)}</td>\n')
            parts.append('                        </tr>\n')

        parts.append('                    </tbody>\n')
        parts.append('                </table>\n')
        parts.append('            </div>\n')

    return ''.join(parts)


def generate_wrestling_html(wrestling_data, title, anchor_id):
    """Generate HTML for a wrestling section."""
    parts = []

    parts.append(f'\n            <h2 class="sport-header" id="{anchor_id}">{esc(title)}</h2>\n')

    weight_classes = wrestling_data.get('weight_classes', [])
    if not weight_classes:
        return ''.join(parts)

    parts.append('            <div class="sport-section">\n')
    parts.append(f'                <h3 class="section-title">Weight Class Rankings</h3>\n')
    parts.append('                <table class="stats-table">\n')
    parts.append('                    <thead>\n')
    parts.append('                        <tr>\n')
    parts.append('                            <th>Weight</th>\n')
    parts.append('                            <th>Rank</th>\n')
    parts.append('                            <th>Wrestler</th>\n')
    parts.append('                            <th>School</th>\n')
    parts.append('                        </tr>\n')
    parts.append('                    </thead>\n')
    parts.append('                    <tbody>\n')

    for wc in weight_classes:
        weight = wc['weight']
        wrestlers = wc['wrestlers']
        for idx, w in enumerate(wrestlers):
            parts.append('                        <tr>\n')
            if idx == 0:
                parts.append(f'                            <td style="font-weight: bold; font-size: 15px;">{esc(weight)}</td>\n')
            else:
                parts.append(f'                            <td></td>\n')
            parts.append(f'                            <td class="rank">{esc(w["rank"])}</td>\n')
            parts.append(f'                            <td>{esc(w["name"])}</td>\n')
            parts.append(f'                            <td>{esc(w["school"])}</td>\n')
            parts.append('                        </tr>\n')

    parts.append('                    </tbody>\n')
    parts.append('                </table>\n')
    parts.append('            </div>\n')

    return ''.join(parts)


def generate_track_html(track_data, title, anchor_id):
    """Generate HTML for indoor track section."""
    parts = []

    parts.append(f'\n            <h2 class="sport-header" id="{anchor_id}">{esc(title)}</h2>\n')

    for gender_key, gender_label in [('boys', 'Boys'), ('girls', 'Girls')]:
        events = track_data.get(gender_key, {})
        if not events:
            continue

        parts.append(f'            <div class="sport-section">\n')
        parts.append(f'                <h3 class="section-title">{esc(gender_label)} Events</h3>\n')
        parts.append('                <table class="stats-table">\n')
        parts.append('                    <thead>\n')
        parts.append('                        <tr>\n')
        parts.append('                            <th>Event</th>\n')
        parts.append('                            <th>Rank</th>\n')
        parts.append('                            <th>Athlete(s)</th>\n')
        parts.append('                            <th>Result</th>\n')
        parts.append('                        </tr>\n')
        parts.append('                    </thead>\n')
        parts.append('                    <tbody>\n')

        for event_name, athletes in events.items():
            for idx, a in enumerate(athletes):
                parts.append('                        <tr>\n')
                if idx == 0:
                    parts.append(f'                            <td style="font-weight: bold;">{esc(event_name)}</td>\n')
                else:
                    parts.append(f'                            <td></td>\n')
                parts.append(f'                            <td class="rank">{idx + 1}</td>\n')
                parts.append(f'                            <td>{esc(a["entry"])}</td>\n')
                parts.append(f'                            <td>{esc(a["result"])}</td>\n')
                parts.append('                        </tr>\n')

        parts.append('                    </tbody>\n')
        parts.append('                </table>\n')
        parts.append('            </div>\n')

    return ''.join(parts)


def generate_swimming_html(swim_data, title, anchor_id):
    """Generate HTML for swimming & diving section."""
    parts = []

    parts.append(f'\n            <h2 class="sport-header" id="{anchor_id}">{esc(title)}</h2>\n')

    for gender_key, gender_label in [('boys', 'Boys'), ('girls', 'Girls')]:
        events = swim_data.get(gender_key, {})
        if not events:
            continue

        parts.append(f'            <div class="sport-section">\n')
        parts.append(f'                <h3 class="section-title">{esc(gender_label)} Events</h3>\n')
        parts.append('                <table class="stats-table">\n')
        parts.append('                    <thead>\n')
        parts.append('                        <tr>\n')
        parts.append('                            <th>Event</th>\n')
        parts.append('                            <th>Rank</th>\n')
        parts.append('                            <th>Athlete(s)</th>\n')
        parts.append('                            <th>Time/Score</th>\n')
        parts.append('                        </tr>\n')
        parts.append('                    </thead>\n')
        parts.append('                    <tbody>\n')

        for event_name, athletes in events.items():
            for idx, a in enumerate(athletes):
                parts.append('                        <tr>\n')
                if idx == 0:
                    parts.append(f'                            <td style="font-weight: bold;">{esc(event_name)}</td>\n')
                else:
                    parts.append(f'                            <td></td>\n')
                parts.append(f'                            <td class="rank">{idx + 1}</td>\n')
                parts.append(f'                            <td>{esc(a["entry"])}</td>\n')
                parts.append(f'                            <td>{esc(a["result"])}</td>\n')
                parts.append('                        </tr>\n')

        parts.append('                    </tbody>\n')
        parts.append('                </table>\n')
        parts.append('            </div>\n')

    return ''.join(parts)


def generate_rankings_html(rankings_data):
    """Generate HTML for power rankings section."""
    parts = []

    parts.append('\n            <h2 class="sport-header" id="rankings">Power Rankings</h2>\n')
    parts.append('            <div class="rankings-grid">\n')

    for sport_name, teams in rankings_data.items():
        if not teams:
            continue

        parts.append('                <div class="ranking-card">\n')
        parts.append(f'                    <h4>{esc(sport_name)}</h4>\n')
        parts.append('                    <ol>\n')
        for team in teams:
            parts.append(f'                        <li>{esc(team["team"])}</li>\n')
        parts.append('                    </ol>\n')
        parts.append('                </div>\n')

    parts.append('            </div>\n')

    return ''.join(parts)


def export_basketball_json(bball_data, data_dir, prefix):
    """Export basketball data as JSON files matching generate_data_js.py schema."""
    leader_key_map = {
        'scoring': ['gp', 'pts', 'avg'],
        'rebounds': ['gp', 'reb', 'avg'],
        'assists': ['gp', 'ast', 'avg'],
    }
    data_json = {}
    for cat_key, keys in leader_key_map.items():
        players = bball_data.get('leaders', {}).get(cat_key, [])
        data_json[cat_key] = []
        for p in players:
            entry = {'player': p['player'], 'school': p['school']}
            for i, k in enumerate(keys):
                entry[k] = p['values'][i] if i < len(p['values']) else ''
            data_json[cat_key].append(entry)

    with open(os.path.join(data_dir, f'{prefix}_data.json'), 'w') as f:
        json.dump(data_json, f, indent=2)

    standings = bball_data.get('standings', {})
    with open(os.path.join(data_dir, f'{prefix}_standings.json'), 'w') as f:
        json.dump(standings, f, indent=2)


def export_wrestling_json(wrestling_data, data_dir, prefix):
    """Export wrestling data as JSON with weight class keys."""
    result = {}
    for wc in wrestling_data.get('weight_classes', []):
        key = f"wc_{wc['weight']}"
        result[key] = [
            {'player': w['name'], 'school': w['school'], 'rank': w['rank']}
            for w in wc['wrestlers']
        ]
    with open(os.path.join(data_dir, f'{prefix}_data.json'), 'w') as f:
        json.dump(result, f, indent=2)


def export_track_json(track_data, data_dir, filename):
    """Export track data as JSON with event keys."""
    result = {}
    for gender in ['boys', 'girls']:
        events = track_data.get(gender, {})
        for event_name, athletes in events.items():
            key = f"{gender}_{event_name.lower().replace(' ', '_').replace(',', '').replace('-', '_')}"
            # Normalize: "55-meter dash" -> "55_meter_dash"
            result[key] = [
                {'player': a['entry'], 'school': '', 'result': a['result']}
                for a in athletes
            ]
    with open(os.path.join(data_dir, filename), 'w') as f:
        json.dump(result, f, indent=2)


def export_swimming_json(swim_data, data_dir, filename):
    """Export swimming data as JSON with event keys."""
    result = {}
    for gender in ['boys', 'girls']:
        events = swim_data.get(gender, {})
        for event_name, athletes in events.items():
            key = f"{gender}_{event_name.lower().replace(' ', '_').replace(',', '').replace('-', '_')}"
            result[key] = [
                {'player': a['entry'], 'school': '', 'result': a['result']}
                for a in athletes
            ]
    with open(os.path.join(data_dir, filename), 'w') as f:
        json.dump(result, f, indent=2)


def export_json_data(data, data_dir):
    """Export all parsed data as JSON files for generate_data_js.py."""
    os.makedirs(data_dir, exist_ok=True)
    export_basketball_json(data['boys_basketball'], data_dir, 'boys_basketball')
    export_basketball_json(data['girls_basketball'], data_dir, 'girls_basketball')
    export_wrestling_json(data['boys_wrestling'], data_dir, 'boys_wrestling')
    export_wrestling_json(data['girls_wrestling'], data_dir, 'girls_wrestling')
    export_track_json(data['indoor_track'], data_dir, 'indoor_track_data.json')
    export_swimming_json(data['swimming'], data_dir, 'swimming_data.json')
    print(f"Exported JSON data to {data_dir}")


def export_rankings_json(rankings_data, data_dir):
    """Export rankings data as JSON for generate_data_js.py to discover."""
    os.makedirs(data_dir, exist_ok=True)
    # Convert to the format expected by generate_data_js.py:
    # [{"sport": "Boys Basketball", "items": [{"team": "Middletown"}, ...]}, ...]
    rankings_list = []
    for sport_name, teams in rankings_data.items():
        rankings_list.append({
            'sport': sport_name,
            'items': [{'team': t['team']} for t in teams]
        })
    with open(os.path.join(data_dir, 'rankings.json'), 'w') as f:
        json.dump(rankings_list, f, indent=2)
    print(f"Exported rankings to {os.path.join(data_dir, 'rankings.json')}")


def extract_date_from_filename(filename):
    """Extract date from hangout filename and return YYYY_MM_DD format.

    Handles patterns like:
        FNPHangoutTextStats2.12.26.txt -> 2026_02_12
        FNPHangoutTextState1.29.26.txt -> 2026_01_29
    """
    match = re.match(r'FNPHangoutText[A-Za-z]*(\d{1,2})\.(\d{1,2})\.(\d{2})\.txt', filename)
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        year = 2000 + int(match.group(3))
        if not (1 <= month <= 12 and 1 <= day <= 31):
            return None
        return f"{year}_{month:02d}_{day:02d}"
    return None


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Parse FNP High School Hangout text file')
    parser.add_argument('--file', type=str, help='Path to the input text file')
    parser.add_argument('--date', type=str, help='Date string in YYYY_MM_DD format (e.g., 2026_02_12)')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    if args.file and args.date:
        input_file = args.file
        date_str = args.date
    else:
        # Default: find the most recent .txt file in hs_hangout/
        hangout_dir = os.path.join(script_dir, 'hs_hangout')
        txt_files = sorted(
            [f for f in os.listdir(hangout_dir) if f.startswith('FNPHangoutText') and f.endswith('.txt')],
            key=lambda f: os.path.getmtime(os.path.join(hangout_dir, f)),
            reverse=True
        )
        if not txt_files:
            print("No hangout text files found in hs_hangout/")
            return
        input_file = os.path.join(hangout_dir, txt_files[0])
        date_str = extract_date_from_filename(txt_files[0])
        if not date_str:
            print(f"Could not extract date from filename: {txt_files[0]}")
            return

    output_file = os.path.join(script_dir, 'docs', f'winter_sports_{date_str}.html')

    print(f"Reading: {input_file}")
    data = parse_hangout_text(input_file)

    # Print summary
    bb = data['boys_basketball']
    gb = data['girls_basketball']
    print(f"Boys Basketball: {len(bb['standings'])} standing divisions, {len(bb['leaders'])} leader categories")
    print(f"Girls Basketball: {len(gb['standings'])} standing divisions, {len(gb['leaders'])} leader categories")
    print(f"Boys Wrestling: {len(data['boys_wrestling']['weight_classes'])} weight classes")
    print(f"Girls Wrestling: {len(data['girls_wrestling']['weight_classes'])} weight classes")
    print(f"Indoor Track: {len(data['indoor_track']['boys'])} boys events, {len(data['indoor_track']['girls'])} girls events")
    print(f"Swimming: {len(data['swimming']['boys'])} boys events, {len(data['swimming']['girls'])} girls events")
    print(f"Rankings: {len(data['rankings'])} sports ranked")

    html_content = generate_html(data, date_str)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\nGenerated: {output_file}")
    print(f"File size: {len(html_content):,} bytes")

    # Export JSON data for the dropdown integration
    data_dir = os.path.join(script_dir, 'data', date_str)
    export_json_data(data, data_dir)

    # Export rankings JSON
    export_rankings_json(data['rankings'], data_dir)


if __name__ == '__main__':
    main()
