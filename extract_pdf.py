#!/usr/bin/env python3
"""
PDF extraction script for Frederick Sports player statistics.
Extracts player stats from the HS Hangout PDF and converts to structured data.
"""

import fitz  # PyMuPDF
import re
import json
from typing import Dict, List, Any, Tuple


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
}


def expand_team_name(team_abbr: str) -> str:
    """
    Expand team abbreviation to full name.

    Args:
        team_abbr: Team abbreviation (e.g., 'Brun.', 'TJ')

    Returns:
        Full team name if abbreviation found, otherwise original string
    """
    return TEAM_ABBREVIATIONS.get(team_abbr, team_abbr)


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

    # Find all SCORING LEADERS and GOALKEEPER STATISTICS sections
    scoring_indices = []
    goalkeeper_indices = []

    for i, line in enumerate(lines):
        if line.strip() == 'SCORING LEADERS':
            scoring_indices.append(i)
        if line.strip() == 'GOALKEEPER STATISTICS':
            goalkeeper_indices.append(i)

    print(f"DEBUG [{sport_name}]: Found {len(scoring_indices)} SCORING LEADERS sections")
    print(f"DEBUG [{sport_name}]: Found {len(goalkeeper_indices)} GOALKEEPER STATISTICS sections")

    # Match each SCORING LEADERS to its GOALKEEPER STATISTICS by position
    # A sport's SCORING section comes before its GOALKEEPER section
    # First GOALKEEPER is always Field Hockey, so skip SCORING sections before it

    first_goalkeeper = goalkeeper_indices[0] if goalkeeper_indices else float('inf')

    # Build pairs of (scoring_idx, goalkeeper_idx) for soccer sections only
    # Soccer SCORING LEADERS come AFTER Field Hockey's GOALKEEPER STATISTICS
    soccer_pairs = []
    for scoring_idx in scoring_indices:
        if scoring_idx > first_goalkeeper:
            # Find the first GOALKEEPER after this SCORING
            for gk_idx in goalkeeper_indices:
                if gk_idx > scoring_idx:
                    soccer_pairs.append((scoring_idx, gk_idx))
                    break

    print(f"DEBUG [{sport_name}]: Found {len(soccer_pairs)} soccer section pairs")

    # Determine which pair is Boys vs Girls by checking player names
    def is_boys_goalkeeper(gk_idx):
        """Check if goalkeeper section has male player names."""
        # Common male first name patterns
        male_indicators = ['Ben ', 'TJ ', 'Andrew ', 'Chris ', 'Michael ', 'David ',
                          'James ', 'John ', 'Robert ', 'William ', 'Ryan ', 'Matt ',
                          'Tyler ', 'Josh ', 'Nick ', 'Mike ', 'Dan ', 'Tom ', 'Joe ']
        for i in range(gk_idx + 1, min(gk_idx + 15, len(lines))):
            line = lines[i].strip()
            if ',' in line and line[0].isalpha():
                player_name = line.split(',')[0].strip()
                if player_name and player_name != 'Player':
                    # Check if name starts with common male indicator
                    for male in male_indicators:
                        if player_name.startswith(male.strip()):
                            return True
                    return False
        return False

    # Find the correct pair for this sport
    scoring_idx = None
    goalkeeper_idx = None

    for pair_scoring, pair_gk in soccer_pairs:
        is_boys = is_boys_goalkeeper(pair_gk)
        if "Boys" in sport_name and is_boys:
            scoring_idx = pair_scoring
            goalkeeper_idx = pair_gk
            break
        elif "Girls" in sport_name and not is_boys:
            scoring_idx = pair_scoring
            goalkeeper_idx = pair_gk
            break

    # Fallback to position-based if name detection failed
    if scoring_idx is None and len(soccer_pairs) >= 2:
        print(f"DEBUG [{sport_name}]: Using fallback position-based matching")
        if "Boys" in sport_name:
            scoring_idx, goalkeeper_idx = soccer_pairs[0]
        else:
            scoring_idx, goalkeeper_idx = soccer_pairs[1]
    elif scoring_idx is None and len(soccer_pairs) == 1:
        scoring_idx, goalkeeper_idx = soccer_pairs[0]

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
            if any(keyword in stripped for keyword in ['FCPS', 'CENTRAL MARYLAND', 'SCORING LEADERS', 'KEEPING TABS']):
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


def parse_field_hockey_stats(text: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Parse field hockey player statistics from extracted text.

    Returns dict with keys: scoring, goalkeepers
    """
    stats = {
        'scoring': [],
        'goalkeepers': []
    }

    # Split text into lines for easier parsing
    lines = text.split('\n')

    # First find the first GOALKEEPER STATISTICS (this is always Field Hockey's)
    goalkeeper_idx = None
    for i, line in enumerate(lines):
        if line.strip() == 'GOALKEEPER STATISTICS':
            goalkeeper_idx = i
            break

    # Find Field Hockey's "Scoring Leaders" section - it comes BEFORE the first GOALKEEPER
    # Match both "Scoring Leaders" (mixed case) and "SCORING LEADERS" (uppercase)
    scoring_idx = None
    if goalkeeper_idx is not None:
        for i, line in enumerate(lines):
            if i >= goalkeeper_idx:
                break
            if line.strip().upper() == 'SCORING LEADERS':
                scoring_idx = i

    print(f"DEBUG [Field Hockey]: Scoring Leaders at line {scoring_idx}")
    print(f"DEBUG [Field Hockey]: GOALKEEPER STATISTICS at line {goalkeeper_idx}")

    # Parse Scoring Leaders
    if scoring_idx is not None:
        print(f"DEBUG [Field Hockey]: Parsing Scoring Leaders at line {scoring_idx}")
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
            if 'Player, School' in stripped or ('GP' in stripped and 'Pts' in stripped):
                continue
            if stripped in ['G', 'A']:
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
        print(f"DEBUG [Field Hockey]: Parsing GOALKEEPER STATISTICS at line {goalkeeper_idx}")
        current_player_lines = []

        def save_goalkeeper():
            if current_player_lines:
                combined = '\t'.join(current_player_lines)
                stats['goalkeepers'].append({'raw': combined})
                current_player_lines.clear()

        for i in range(goalkeeper_idx, len(lines)):
            stripped = lines[i].strip()

            # Stop conditions
            if any(keyword in stripped for keyword in ['FCPS', 'CENTRAL MARYLAND', 'INDIVIDUAL LEADERS']):
                save_goalkeeper()
                break

            # Skip headers
            if 'Player, School' in stripped or ('GP' in stripped and 'GAA' in stripped):
                continue
            if 'GA' in stripped and 'SO' in stripped and 'SV%' in stripped:
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


def parse_field_hockey_player_entry(raw: str, stat_type: str) -> Dict[str, Any]:
    """
    Parse a raw field hockey player entry into structured data.

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


def parse_cross_country_stats(text: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Parse cross country player statistics from extracted text.

    Returns dict with keys: boys, girls
    """
    stats = {
        'boys': [],
        'girls': []
    }

    # Split text into lines for easier parsing
    lines = text.split('\n')

    # Find "Top 5K Times" section (case-insensitive)
    top_5k_idx = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.upper() == 'TOP 5K TIMES':
            top_5k_idx = i
            break

    if top_5k_idx is None:
        print("DEBUG [Cross Country]: No 'Top 5K Times' section found")
        return stats

    print(f"DEBUG [Cross Country]: Found 'Top 5K Times' at line {top_5k_idx}")

    # Find BOYS and GIRLS sections
    boys_idx = None
    girls_idx = None

    for i in range(top_5k_idx, len(lines)):
        stripped = lines[i].strip()
        if stripped == 'BOYS':
            boys_idx = i
            print(f"DEBUG [Cross Country]: Found BOYS section at line {i}")
        elif stripped == 'GIRLS':
            girls_idx = i
            print(f"DEBUG [Cross Country]: Found GIRLS section at line {i}")
            break

    # Parse Boys section
    if boys_idx is not None and girls_idx is not None:
        for i in range(boys_idx + 1, girls_idx):
            stripped = lines[i].strip()
            if not stripped or 'Staff photo' in stripped:
                continue
            # Parse line: "Name, School, Time"
            if ',' in stripped:
                parts = stripped.split(',')
                if len(parts) >= 3:
                    name = parts[0].strip()
                    school = parts[1].strip()
                    time = parts[2].strip()
                    stats['boys'].append({'raw': stripped})

    # Parse Girls section
    if girls_idx is not None:
        for i in range(girls_idx + 1, len(lines)):
            stripped = lines[i].strip()
            # Stop at next major section
            if any(keyword in stripped for keyword in ['CENTRAL MARYLAND', 'FCPS', 'Staff photo']):
                break
            if not stripped:
                continue
            # Parse line: "Name, School, Time"
            if ',' in stripped:
                parts = stripped.split(',')
                if len(parts) >= 3:
                    name = parts[0].strip()
                    school = parts[1].strip()
                    time = parts[2].strip()
                    stats['girls'].append({'raw': stripped})

    print(f"DEBUG [Cross Country]: Parsed {len(stats['boys'])} boys and {len(stats['girls'])} girls")
    return stats


def parse_cross_country_player_entry(raw: str) -> Dict[str, Any]:
    """
    Parse a raw cross country player entry into structured data.

    Args:
        raw: Raw text like "Joshua Rothery, Urbana, 16:00.4"

    Returns:
        Dict with player name, school, and time
    """
    if ',' not in raw:
        return None

    parts = raw.split(',')
    if len(parts) < 3:
        return None

    player_name = parts[0].strip()
    school = parts[1].strip()
    time = parts[2].strip()

    return {
        'player': player_name,
        'school': school,
        'time': time
    }


def parse_golf_stats(text: str) -> List[Dict[str, Any]]:
    """
    Parse golf player statistics from extracted text.

    Returns list of player stats
    """
    stats = []

    # Split text into lines for easier parsing
    lines = text.split('\n')

    # Find Golf section - look for "Player, School" followed by "9-hole Average"
    golf_idx = None
    for i, line in enumerate(lines):
        if 'Player, School' in line:
            # Check if next line has "9-hole Average"
            if i + 1 < len(lines) and '9-hole' in lines[i + 1]:
                golf_idx = i
                break

    if golf_idx is None:
        print("DEBUG [Golf]: No golf section found")
        return stats

    print(f"DEBUG [Golf]: Found golf section at line {golf_idx}")

    # Parse golf entries starting after the header lines
    # Skip "Player, School" and "9-hole Average" lines
    for i in range(golf_idx + 2, len(lines)):
        stripped = lines[i].strip()

        # Stop conditions
        if any(keyword in stripped for keyword in ['CENTRAL MARYLAND', 'FCPS', 'Staff photo', 'SPIRES DIVISION', 'POTOMAC DIVISION']):
            break

        if not stripped:
            continue

        # Golf entries have format: "Name, School" on one line, average on next
        # Collect player line and next line with average
        if ',' in stripped and not any(char.isdigit() for char in stripped[-5:]):
            # This is a player name line, get the average from next line
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # Check if next line is a number (the average)
                try:
                    float(next_line)
                    # Combine player line with average
                    stats.append({'raw': f"{stripped}\t{next_line}"})
                except ValueError:
                    # Not a number, might be combined on same line
                    stats.append({'raw': stripped})

    print(f"DEBUG [Golf]: Parsed {len(stats)} golf entries")
    return stats


def parse_golf_player_entry(raw: str) -> Dict[str, Any]:
    """
    Parse a raw golf player entry into structured data.

    Args:
        raw: Raw text like "Landon Tudor, Oakdale 35" or "Landon Tudor, Oakdale\t35"

    Returns:
        Dict with player name, school, and average
    """
    if ',' not in raw:
        return None

    # First split by comma to get name and rest
    parts = raw.split(',', 1)
    player_name = parts[0].strip()
    rest = parts[1].strip()

    # Now split rest to get school and average
    # Try tab delimiter first, then spaces
    tokens = re.split(r'[\t\s]+', rest)
    tokens = [t.strip() for t in tokens if t.strip()]

    if not tokens:
        return None

    # Last token should be the average (number)
    average = tokens[-1] if tokens else ''
    # Everything else is the school name
    school = ' '.join(tokens[:-1]) if len(tokens) > 1 else tokens[0]

    return {
        'player': player_name,
        'school': school,
        'average': average
    }


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


def structure_field_hockey_stats(raw_stats: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
    """Convert raw field hockey stats to structured format."""
    structured = {
        'scoring': [],
        'goalkeepers': []
    }

    for stat_type in ['scoring', 'goalkeepers']:
        for entry in raw_stats[stat_type]:
            parsed = parse_field_hockey_player_entry(entry['raw'], stat_type)
            if parsed:
                structured[stat_type].append(parsed)

    return structured


def structure_cross_country_stats(raw_stats: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
    """Convert raw cross country stats to structured format."""
    structured = {
        'boys': [],
        'girls': []
    }

    for gender in ['boys', 'girls']:
        for entry in raw_stats[gender]:
            parsed = parse_cross_country_player_entry(entry['raw'])
            if parsed:
                structured[gender].append(parsed)

    return structured


def structure_golf_stats(raw_stats: List[Dict]) -> List[Dict]:
    """Convert raw golf stats to structured format."""
    structured = []

    for entry in raw_stats:
        parsed = parse_golf_player_entry(entry['raw'])
        if parsed:
            structured.append(parsed)

    return structured


def parse_fcps_standings(text: str, section_index: int = 0) -> List[Dict[str, str]]:
    """
    Parse FCPS conference standings.

    Format:
    FCPS
    Team    W    L    PF    PA
    Linganore
    13
    3
    400
    127

    Note: PDF extraction may produce tab-merged data like "Thomas Johnson\t7"
    where the team name and first stat value are on the same line.

    Args:
        text: The PDF text content
        section_index: Which FCPS section to parse (0=first, 1=second, etc.)
                      Girls Flag Football uses section 0, Football uses section 1
    """
    standings = []
    lines = text.split('\n')

    # Find all FCPS sections
    fcps_sections = []
    for i, line in enumerate(lines):
        if line.strip() == 'FCPS':
            fcps_sections.append(i)

    if section_index >= len(fcps_sections):
        return standings

    fcps_start = fcps_sections[section_index]

    # Skip header lines (FCPS, Team, W, L, PF, PA)
    i = fcps_start + 6  # Skip FCPS + column headers (Team, W, L, PF, PA) - 6 header lines total

    # Collect all values first, handling tabs
    values = []
    while i < len(lines):
        line = lines[i].strip()

        # Stop at next major section
        if any(keyword in line for keyword in ['INDIVIDUAL LEADERS', 'CENTRAL MARYLAND', 'OTHER SCHOOLS', 'PASSING', 'RUSHING']):
            break

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Split by tabs and clean up whitespace
        parts = [p.strip() for p in line.split('\t') if p.strip()]
        values.extend(parts)
        i += 1

    # Now parse the collected values in groups of 5 (team, w, l, pf, pa)
    idx = 0
    while idx + 4 < len(values):
        # Find next team name (non-numeric value)
        if not values[idx].replace('.', '').replace(',', '').isdigit():
            team_name = expand_team_name(values[idx])

            # Next 4 values should be stats
            try:
                wins = values[idx + 1]
                losses = values[idx + 2]
                pf = values[idx + 3]
                pa = values[idx + 4]

                # Validate that these look like numbers
                if (wins.replace(',', '').isdigit() and
                    losses.replace(',', '').isdigit() and
                    pf.replace(',', '').isdigit() and
                    pa.replace(',', '').isdigit()):
                    standings.append({
                        'team': team_name,
                        'wins': wins,
                        'losses': losses,
                        'pf': pf,
                        'pa': pa
                    })
                    idx += 5
                    continue
            except (IndexError, ValueError):
                pass

        idx += 1

    return standings


def parse_central_maryland_standings(text: str, sport_name: str = "Volleyball", section_index: int = 0) -> Dict[str, List[Dict[str, str]]]:
    """
    Parse CENTRAL MARYLAND CONFERENCE standings.

    Format varies by sport:
    - Volleyball/Field Hockey: Division and Overall records, organized by divisions
    - Soccer: Division and Overall records, organized by divisions (W, L, T format)

    Note: PDF extraction may produce tab-merged data. Values are collected and
    then parsed in groups.

    Args:
        text: The PDF text content
        sport_name: Name of the sport (for logging)
        section_index: Which CMC section to parse (0=Boys Soccer, 1=Girls Soccer,
                      2=Volleyball, 3=Field Hockey)

    Returns dict with division names as keys and team lists as values.
    """
    standings = {}
    lines = text.split('\n')

    # Find all CENTRAL MARYLAND CONFERENCE sections
    cmc_sections = []
    for i, line in enumerate(lines):
        if 'CENTRAL MARYLAND CONFERENCE' in line:
            cmc_sections.append(i)

    if section_index >= len(cmc_sections):
        return standings

    cm_start = cmc_sections[section_index]

    # Collect all lines in the section
    section_lines = []
    i = cm_start + 1
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Stop at next major section
        if any(keyword in stripped for keyword in ['INDIVIDUAL LEADERS', 'FCPS', 'OTHER SCHOOLS', 'PASSING', 'RUSHING', 'SCORING']):
            break

        section_lines.append(line)
        i += 1

    # Flatten all values, splitting on tabs
    values = []
    for line in section_lines:
        parts = [p.strip() for p in line.split('\t') if p.strip()]
        values.extend(parts)

    # Clean out header words
    header_words = {'Team', 'W', 'L', 'T', 'Division', 'Overall'}
    values = [v for v in values if v not in header_words]

    # Parse values
    current_division = None
    idx = 0

    while idx < len(values):
        val = values[idx]

        # Check for division headers
        if 'DIVISION' in val or 'SCHOOL' in val:
            # Clean up division name (remove trailing tabs/spaces)
            current_division = val.strip()
            standings[current_division] = []
            idx += 1
            continue

        # Check if this is a team name (starts with letter, not all digits)
        if current_division is not None and not val.replace('.', '').replace(',', '').isdigit():
            team_name = expand_team_name(val)

            # Collect numeric values for this team (Division W, L, T; Overall W, L, T)
            # We expect 6 numeric values: div_w, div_l, div_t, overall_w, overall_l, overall_t
            stats = []
            j = idx + 1
            while j < len(values) and len(stats) < 6:
                next_val = values[j]
                # Stop if we hit another team name or division header
                if ('DIVISION' in next_val or 'SCHOOL' in next_val or
                    (not next_val.replace('.', '').replace(',', '').isdigit() and
                     next_val not in header_words)):
                    break
                if next_val.replace(',', '').isdigit():
                    stats.append(next_val)
                j += 1

            # If we got at least division W and L (first 2 values), record the team
            if len(stats) >= 2:
                div_wins = stats[0]
                div_losses = stats[1]
                # Overall might be partial or missing
                overall_wins = stats[3] if len(stats) > 3 else stats[2] if len(stats) > 2 else ''
                overall_losses = stats[4] if len(stats) > 4 else ''

                standings[current_division].append({
                    'team': team_name,
                    'div_wins': div_wins,
                    'div_losses': div_losses,
                    'overall_wins': overall_wins,
                    'overall_losses': overall_losses
                })
                idx = j
                continue

        idx += 1

    return standings


def parse_other_schools_standings(text: str) -> List[Dict[str, str]]:
    """
    Parse OTHER SCHOOLS standings.

    Format:
    OTHER SCHOOLS
    Team    W    L
    MSD
    18
    1

    Note: PDF extraction may produce tab-merged data.
    """
    standings = []
    lines = text.split('\n')

    # Find OTHER SCHOOLS section
    os_start = -1
    for i, line in enumerate(lines):
        if 'OTHER SCHOOLS' in line:
            os_start = i
            break

    if os_start == -1:
        return standings

    # Collect all lines in the section
    section_lines = []
    i = os_start + 1
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Stop at next major section
        if any(keyword in stripped for keyword in ['INDIVIDUAL LEADERS', 'CENTRAL MARYLAND', 'FCPS', 'PASSING', 'RUSHING', 'SCORING']):
            break

        section_lines.append(line)
        i += 1

    # Flatten all values, splitting on tabs
    values = []
    for line in section_lines:
        parts = [p.strip() for p in line.split('\t') if p.strip()]
        values.extend(parts)

    # Clean out header words
    header_words = {'Team', 'W', 'L'}
    values = [v for v in values if v not in header_words]

    # Parse values in groups of 3 (team, w, l)
    idx = 0
    while idx < len(values):
        val = values[idx]

        # Check if this is a team name (not just a number)
        if not val.replace('.', '').replace(',', '').isdigit():
            team_name = expand_team_name(val)

            # Next 2 values should be wins and losses
            if idx + 2 < len(values):
                try:
                    wins = values[idx + 1]
                    losses = values[idx + 2]

                    if wins.replace(',', '').isdigit() and losses.replace(',', '').isdigit():
                        standings.append({
                            'team': team_name,
                            'wins': wins,
                            'losses': losses
                        })
                        idx += 3
                        continue
                except:
                    pass

        idx += 1

    return standings


def generate_html(stats: Dict[str, List[Dict]], sport: str = "Football", defensive_stats: List[Dict[str, Any]] = None, publish_date: str = "Oct 23, 2025", updated_date: str = "October 21, 2025", standings: List[Dict[str, str]] = None) -> str:
    """Generate HTML page for player stats and standings."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sport} Player Stats - High School Hangout ({publish_date})</title>
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
            <p class="subtitle">Updated Through {updated_date}</p>
            <p class="subtitle">Source: The Frederick News-Post High School Hangout</p>
        </header>

        <main>
"""

    # FCPS Standings (for Football and Girls Flag Football)
    if standings:
        html += """
            <div class="sport-section">
                <h2 class="section-title">FCPS Standings</h2>
                <table class="stats-table">
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
        for team in standings:
            html += f"""                        <tr>
                            <td>{expand_team_name(team.get('team', ''))}</td>
                            <td>{team.get('wins', '')}</td>
                            <td>{team.get('losses', '')}</td>
                            <td>{team.get('pf', '')}</td>
                            <td>{team.get('pa', '')}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
            </div>
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
                            <td>{expand_team_name(player.get('school', ''))}</td>
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
                            <td>{expand_team_name(player.get('school', ''))}</td>
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
                            <td>{expand_team_name(player.get('school', ''))}</td>
                            <td>{player.get('rec', '')}</td>
                            <td>{player.get('yds', '')}</td>
                            <td>{player.get('td', '')}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
            </div>
"""

    # Defensive Leaders (if provided)
    if defensive_stats:
        html += """
            <div class="sport-section">
                <h2 class="section-title">Defensive Leaders</h2>
                <table class="stats-table">
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>School</th>
                            <th>Tkl</th>
                            <th>TFL</th>
                            <th>Int</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for player in defensive_stats:
            html += f"""                        <tr>
                            <td>{player.get('player', '')}</td>
                            <td>{expand_team_name(player.get('school', ''))}</td>
                            <td>{player.get('tkl', '')}</td>
                            <td>{player.get('tfl', '')}</td>
                            <td>{player.get('int', '')}</td>
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
            <p>Att = Attempts, Yds = Yards, Avg = Average, TD = Touchdowns, Comp = Completions, Pct = Completion Percentage, Rec = Receptions, Tkl = Tackles, TFL = Tackles for Loss, Int = Interceptions</p>
            <p><strong>Data Source:</strong> The Frederick News-Post - High School Hangout</p>
            <p>Statistics submitted by coaches and team statisticians</p>
        </footer>
    </div>
</body>
</html>
"""

    return html


def generate_soccer_html(stats: Dict[str, List[Dict]], sport: str = "Boys Soccer", publish_date: str = "Oct 23, 2025", updated_date: str = "October 21, 2025", standings: Dict[str, List[Dict[str, str]]] = None) -> str:
    """Generate HTML page for soccer player stats and standings."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sport} Player Stats - High School Hangout ({publish_date})</title>
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
            <p class="subtitle">Updated Through {updated_date}</p>
            <p class="subtitle">Source: The Frederick News-Post High School Hangout</p>
        </header>

        <main>
"""

    # Central Maryland Conference Standings
    if standings:
        for division_name, teams in standings.items():
            if teams:  # Only show divisions that have teams
                html += f"""
            <div class="sport-section">
                <h2 class="section-title">{division_name}</h2>
                <table class="stats-table">
                    <thead>
                        <tr>
                            <th>Team</th>
                            <th colspan="2">Division</th>
                            <th colspan="2">Overall</th>
                        </tr>
                        <tr>
                            <th></th>
                            <th>W</th>
                            <th>L</th>
                            <th>W</th>
                            <th>L</th>
                        </tr>
                    </thead>
                    <tbody>
"""
                for team in teams:
                    html += f"""                        <tr>
                            <td>{expand_team_name(team.get('team', ''))}</td>
                            <td>{team.get('div_wins', '')}</td>
                            <td>{team.get('div_losses', '')}</td>
                            <td>{team.get('overall_wins', '')}</td>
                            <td>{team.get('overall_losses', '')}</td>
                        </tr>
"""
                html += """                    </tbody>
                </table>
            </div>
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
                            <td>{expand_team_name(player.get('school', ''))}</td>
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
                            <td>{expand_team_name(player.get('school', ''))}</td>
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


def generate_volleyball_html(stats: Dict[str, List[Dict]], sport: str = "Volleyball", publish_date: str = "Oct 23, 2025", updated_date: str = "October 21, 2025", standings: Dict[str, List[Dict[str, str]]] = None) -> str:
    """Generate HTML page for volleyball player stats and standings."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sport} Player Stats - High School Hangout ({publish_date})</title>
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
            <p class="subtitle">Updated Through {updated_date}</p>
            <p class="subtitle">Source: The Frederick News-Post High School Hangout</p>
        </header>

        <main>
"""

    # Central Maryland Conference Standings
    if standings:
        for division_name, teams in standings.items():
            if teams:  # Only show divisions that have teams
                html += f"""
            <div class="sport-section">
                <h2 class="section-title">{division_name}</h2>
                <table class="stats-table">
                    <thead>
                        <tr>
                            <th>Team</th>
                            <th colspan="2">Division</th>
                            <th colspan="2">Overall</th>
                        </tr>
                        <tr>
                            <th></th>
                            <th>W</th>
                            <th>L</th>
                            <th>W</th>
                            <th>L</th>
                        </tr>
                    </thead>
                    <tbody>
"""
                for team in teams:
                    html += f"""                        <tr>
                            <td>{expand_team_name(team.get('team', ''))}</td>
                            <td>{team.get('div_wins', '')}</td>
                            <td>{team.get('div_losses', '')}</td>
                            <td>{team.get('overall_wins', '')}</td>
                            <td>{team.get('overall_losses', '')}</td>
                        </tr>
"""
                html += """                    </tbody>
                </table>
            </div>
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
                            <td>{expand_team_name(player.get('school', ''))}</td>
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
                            <td>{expand_team_name(player.get('school', ''))}</td>
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
                            <td>{expand_team_name(player.get('school', ''))}</td>
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


def generate_field_hockey_html(stats: Dict[str, List[Dict]], sport: str = "Field Hockey", publish_date: str = "Oct 23, 2025", updated_date: str = "October 21, 2025", standings: Dict[str, List[Dict[str, str]]] = None) -> str:
    """Generate HTML page for field hockey player stats and standings."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sport} Player Stats - High School Hangout ({publish_date})</title>
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
            <p class="subtitle">Updated Through {updated_date}</p>
            <p class="subtitle">Source: The Frederick News-Post High School Hangout</p>
        </header>

        <main>
"""

    # Central Maryland Conference Standings
    if standings:
        for division_name, teams in standings.items():
            if teams:  # Only show divisions that have teams
                html += f"""
            <div class="sport-section">
                <h2 class="section-title">{division_name}</h2>
                <table class="stats-table">
                    <thead>
                        <tr>
                            <th>Team</th>
                            <th colspan="2">Division</th>
                            <th colspan="2">Overall</th>
                        </tr>
                        <tr>
                            <th></th>
                            <th>W</th>
                            <th>L</th>
                            <th>W</th>
                            <th>L</th>
                        </tr>
                    </thead>
                    <tbody>
"""
                for team in teams:
                    html += f"""                        <tr>
                            <td>{expand_team_name(team.get('team', ''))}</td>
                            <td>{team.get('div_wins', '')}</td>
                            <td>{team.get('div_losses', '')}</td>
                            <td>{team.get('overall_wins', '')}</td>
                            <td>{team.get('overall_losses', '')}</td>
                        </tr>
"""
                html += """                    </tbody>
                </table>
            </div>
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
                            <td>{expand_team_name(player.get('school', ''))}</td>
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
                            <td>{expand_team_name(player.get('school', ''))}</td>
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


def generate_cross_country_html(stats: Dict[str, List[Dict]], sport: str = "Cross Country", publish_date: str = "Oct 23, 2025", updated_date: str = "October 21, 2025") -> str:
    """Generate HTML page for cross country player stats."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sport} Top Times - High School Hangout ({publish_date})</title>
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

        .rank {{
            color: #666;
            font-weight: bold;
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
            <h1>{sport} Top 5K Times</h1>
            <p class="subtitle">Updated Through {updated_date}</p>
            <p class="subtitle">Source: The Frederick News-Post High School Hangout</p>
        </header>

        <main>
"""

    # Boys Top Times
    if stats.get('boys'):
        html += """
            <div class="sport-section">
                <h2 class="section-title">Boys Top 5K Times</h2>
                <table class="stats-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Runner</th>
                            <th>School</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for idx, runner in enumerate(stats['boys'], 1):
            html += f"""                        <tr>
                            <td class="rank">{idx}</td>
                            <td>{runner.get('player', '')}</td>
                            <td>{expand_team_name(runner.get('school', ''))}</td>
                            <td>{runner.get('time', '')}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
            </div>
"""

    # Girls Top Times
    if stats.get('girls'):
        html += """
            <div class="sport-section">
                <h2 class="section-title">Girls Top 5K Times</h2>
                <table class="stats-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Runner</th>
                            <th>School</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for idx, runner in enumerate(stats['girls'], 1):
            html += f"""                        <tr>
                            <td class="rank">{idx}</td>
                            <td>{runner.get('player', '')}</td>
                            <td>{expand_team_name(runner.get('school', ''))}</td>
                            <td>{runner.get('time', '')}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
            </div>
"""

    html += """
        </main>

        <footer>
            <p><strong>Note:</strong> Times are for 5K (5000 meter) races</p>
            <p><strong>Data Source:</strong> The Frederick News-Post - High School Hangout</p>
            <p>Statistics submitted by coaches and team statisticians</p>
        </footer>
    </div>
</body>
</html>
"""

    return html


def generate_golf_html(stats: List[Dict], sport: str = "Golf", publish_date: str = "Oct 23, 2025", updated_date: str = "October 21, 2025") -> str:
    """Generate HTML page for golf player stats."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sport} Player Stats - High School Hangout ({publish_date})</title>
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
            max-width: 1000px;
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
            <h1>{sport} Player Leaders</h1>
            <p class="subtitle">Updated Through {updated_date}</p>
            <p class="subtitle">Source: The Frederick News-Post High School Hangout</p>
        </header>

        <main>
            <div class="sport-section">
                <h2 class="section-title">9-Hole Scoring Average</h2>
                <table class="stats-table">
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>School</th>
                            <th>Average</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    for player in stats:
        html += f"""                        <tr>
                            <td>{player.get('player', '')}</td>
                            <td>{expand_team_name(player.get('school', ''))}</td>
                            <td>{player.get('average', '')}</td>
                        </tr>
"""

    html += """                    </tbody>
                </table>
            </div>
        </main>

        <footer>
            <p><strong>Note:</strong> Average scores are for 9-hole rounds</p>
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
    with open(f'{raw_filename}', 'w') as f:
        json.dump(stats_raw, f, indent=2)

    # Structure the stats
    print(f"\nStructuring data...")
    stats = structure_stats(stats_raw)

    # Save structured stats
    stats_filename = f'{file_prefix}_stats.json'
    with open(f'{stats_filename}', 'w') as f:
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

    # Load defensive stats if this is Girls Flag Football
    defensive_stats = None
    if sport_name == "Girls Flag Football":
        print(f"\nLoading defensive stats...")
        defensive_stats = parse_defensive_stats()
        if defensive_stats:
            print(f"  Loaded {len(defensive_stats)} defensive stat entries")

    # Generate HTML
    print(f"\nGenerating HTML page...")
    html = generate_html(stats, sport_name, defensive_stats=defensive_stats)

    # Save HTML to both hs_hangout and docs directories
    html_filename = f'player_stats_{file_prefix}_2025_12_06.html'
    output_path_hs = f'hs_hangout/{html_filename}'
    output_path_docs = f'docs/{html_filename}'

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
    with open(f'{raw_filename}', 'w') as f:
        json.dump(stats_raw, f, indent=2)

    # Structure the stats
    print(f"\nStructuring data...")
    stats = structure_soccer_stats(stats_raw)

    # Save structured stats
    stats_filename = f'{file_prefix}_stats.json'
    with open(f'{stats_filename}', 'w') as f:
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
    html_filename = f'player_stats_{file_prefix}_2025_12_06.html'
    output_path_hs = f'hs_hangout/{html_filename}'
    output_path_docs = f'docs/{html_filename}'

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
    with open(f'{raw_filename}', 'w') as f:
        json.dump(stats_raw, f, indent=2)

    # Structure the stats
    print(f"\nStructuring data...")
    stats = structure_volleyball_stats(stats_raw)

    # Save structured stats
    stats_filename = f'{file_prefix}_stats.json'
    with open(f'{stats_filename}', 'w') as f:
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
    html_filename = f'player_stats_{file_prefix}_2025_12_06.html'
    output_path_hs = f'hs_hangout/{html_filename}'
    output_path_docs = f'docs/{html_filename}'

    with open(output_path_hs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_hs}")

    with open(output_path_docs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_docs}")

    print(f"\n✓ {sport_name} player stats extraction and HTML generation complete!")


def process_field_hockey_sport(text: str):
    """Process field hockey stats."""
    sport_name = "Field Hockey"
    file_prefix = "field_hockey"

    print(f"\n{'='*60}")
    print(f"Processing {sport_name}")
    print(f"{'='*60}")

    # Parse stats
    print(f"\nParsing {sport_name} statistics...")
    stats_raw = parse_field_hockey_stats(text)

    # Save raw stats
    raw_filename = f'{file_prefix}_stats_raw.json'
    with open(f'{raw_filename}', 'w') as f:
        json.dump(stats_raw, f, indent=2)

    # Structure the stats
    print(f"\nStructuring data...")
    stats = structure_field_hockey_stats(stats_raw)

    # Save structured stats
    stats_filename = f'{file_prefix}_stats.json'
    with open(f'{stats_filename}', 'w') as f:
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
    html = generate_field_hockey_html(stats, sport_name)

    # Save HTML to both hs_hangout and docs directories
    html_filename = f'player_stats_{file_prefix}_2025_12_06.html'
    output_path_hs = f'hs_hangout/{html_filename}'
    output_path_docs = f'docs/{html_filename}'

    with open(output_path_hs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_hs}")

    with open(output_path_docs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_docs}")

    print(f"\n✓ {sport_name} player stats extraction and HTML generation complete!")


def process_cross_country_sport(text: str):
    """Process cross country stats."""
    sport_name = "Cross Country"
    file_prefix = "cross_country"

    print(f"\n{'='*60}")
    print(f"Processing {sport_name}")
    print(f"{'='*60}")

    # Parse stats
    print(f"\nParsing {sport_name} statistics...")
    stats_raw = parse_cross_country_stats(text)

    # Save raw stats
    raw_filename = f'{file_prefix}_stats_raw.json'
    with open(f'{raw_filename}', 'w') as f:
        json.dump(stats_raw, f, indent=2)

    # Structure the stats
    print(f"\nStructuring data...")
    stats = structure_cross_country_stats(stats_raw)

    # Save structured stats
    stats_filename = f'{file_prefix}_stats.json'
    with open(f'{stats_filename}', 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\n{sport_name} stats parsed:")
    print(f"  Boys top times: {len(stats['boys'])} entries")
    print(f"  Girls top times: {len(stats['girls'])} entries")

    # Show sample data
    if stats['boys']:
        print(f"\nSample boys leader:")
        leader = stats['boys'][0]
        print(f"  {leader.get('player', 'N/A')}, {leader.get('school', 'N/A')}")
        print(f"  Time: {leader.get('time', 'N/A')}")

    print(f"\nStats saved to {stats_filename}")

    # Generate HTML
    print(f"\nGenerating HTML page...")
    html = generate_cross_country_html(stats, sport_name)

    # Save HTML to both hs_hangout and docs directories
    html_filename = f'{file_prefix}_2025_12_06.html'
    output_path_hs = f'hs_hangout/{html_filename}'
    output_path_docs = f'docs/{html_filename}'

    with open(output_path_hs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_hs}")

    with open(output_path_docs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_docs}")

    print(f"\n✓ {sport_name} stats extraction and HTML generation complete!")


def process_golf_sport(text: str):
    """Process golf stats."""
    sport_name = "Golf"
    file_prefix = "golf"

    print(f"\n{'='*60}")
    print(f"Processing {sport_name}")
    print(f"{'='*60}")

    # Parse stats
    print(f"\nParsing {sport_name} statistics...")
    stats_raw = parse_golf_stats(text)

    # Save raw stats
    raw_filename = f'{file_prefix}_stats_raw.json'
    with open(f'{raw_filename}', 'w') as f:
        json.dump(stats_raw, f, indent=2)

    # Structure the stats
    print(f"\nStructuring data...")
    stats = structure_golf_stats(stats_raw)

    # Save structured stats
    stats_filename = f'{file_prefix}_stats.json'
    with open(f'{stats_filename}', 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\n{sport_name} stats parsed:")
    print(f"  Player leaders: {len(stats)} entries")

    # Show sample data
    if stats:
        print(f"\nSample leader:")
        leader = stats[0]
        print(f"  {leader.get('player', 'N/A')}, {leader.get('school', 'N/A')}")
        print(f"  Average: {leader.get('average', 'N/A')}")

    print(f"\nStats saved to {stats_filename}")

    # Generate HTML
    print(f"\nGenerating HTML page...")
    html = generate_golf_html(stats, sport_name)

    # Save HTML to both hs_hangout and docs directories
    html_filename = f'{file_prefix}_2025_12_06.html'
    output_path_hs = f'hs_hangout/{html_filename}'
    output_path_docs = f'docs/{html_filename}'

    with open(output_path_hs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_hs}")

    with open(output_path_docs, 'w') as f:
        f.write(html)
    print(f"HTML saved to: {output_path_docs}")

    print(f"\n✓ {sport_name} stats extraction and HTML generation complete!")


def parse_defensive_stats(file_path: str = 'FlagDefenseStats.txt') -> List[Dict[str, Any]]:
    """
    Parse defensive stats from the FlagDefenseStats.txt file.

    Returns:
        List of dicts with player defensive statistics
    """
    defensive_stats = []

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Skip header lines and parse data
        for line in lines[3:]:  # Skip "Defense", blank line, and column headers
            line = line.strip()
            if not line:
                continue

            # Split by semicolon
            parts = line.split(';')
            if len(parts) != 4:
                continue

            # Parse player and school
            player_school = parts[0].strip()
            if ',' in player_school:
                player, school = player_school.split(',', 1)
                player = player.strip()
                school = school.strip()
            else:
                continue

            # Parse stats: Tkl, TFL, Int
            tkl_val = parts[1].strip()
            tfl_val = parts[2].strip()
            int_val = parts[3].strip()

            defensive_stats.append({
                'player': player,
                'school': school,
                'tkl': tkl_val if tkl_val != '-' else '0',
                'tfl': tfl_val if tfl_val != '-' else '0',
                'int': int_val if int_val != '-' else '0'
            })

        print(f"DEBUG: Parsed {len(defensive_stats)} defensive stats entries")

    except FileNotFoundError:
        print(f"Warning: {file_path} not found, skipping defensive stats")
    except Exception as e:
        print(f"Error parsing defensive stats: {e}")

    return defensive_stats


def main():
    """Main extraction function."""
    pdf_path = 'hs_hangout/2025_12_06.pdf'

    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)

    # Save full text for inspection
    with open('pdf_text.txt', 'w') as f:
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

    # Process field hockey
    process_field_hockey_sport(text)

    # Process cross country
    process_cross_country_sport(text)

    # Process golf
    process_golf_sport(text)

    print(f"\n{'='*60}")
    print("ALL SPORTS COMPLETE!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
