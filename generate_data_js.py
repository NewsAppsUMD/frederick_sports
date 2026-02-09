#!/usr/bin/env python3
"""
Generate data.js file for the web frontend from JSON data files.
Combines data from multiple dates into a single JavaScript module.
"""

import json
from pathlib import Path
from datetime import datetime
from generate_embed_html import generate_all_embeds

# Configuration
DATA_DIR = Path('data')
OUTPUT_FILE = Path('docs/data.js')

# Date configurations
DATES = [
    {'value': '2025_10_23', 'label': 'Oct 23, 2025'},
    {'value': '2025_12_06', 'label': 'Dec 6, 2025'},
    {'value': '2026_01_29', 'label': 'Jan 29, 2026'},
]

# Sport configurations
SPORTS_CONFIG = {
    'football': {
        'name': 'Football',
        'file': 'football_data.json',
        'standings_file': 'football_standings.json',
        'standings_type': 'fcps',  # FCPS conference with W/L/PF/PA
        'leaders': [
            {
                'categoryName': 'Rushing',
                'source': 'rushing',
                'headers': [
                    {'key': 'att', 'label': 'Att'},
                    {'key': 'yds', 'label': 'Yds'},
                    {'key': 'avg', 'label': 'Avg'},
                    {'key': 'td', 'label': 'TD'}
                ]
            },
            {
                'categoryName': 'Passing',
                'source': 'passing',
                'headers': [
                    {'key': 'comp', 'label': 'Comp'},
                    {'key': 'att', 'label': 'Att'},
                    {'key': 'pct', 'label': 'Pct'},
                    {'key': 'yds', 'label': 'Yds'},
                    {'key': 'td', 'label': 'TD'}
                ]
            },
            {
                'categoryName': 'Receiving',
                'source': 'receiving',
                'headers': [
                    {'key': 'rec', 'label': 'Rec'},
                    {'key': 'yds', 'label': 'Yds'},
                    {'key': 'td', 'label': 'TD'}
                ]
            }
        ]
    },
    'girls-flag-football': {
        'name': 'Girls Flag Football',
        'file': 'girls_flag_football_data.json',
        'standings_file': 'girls_flag_football_standings.json',
        'standings_type': 'fcps',
        'leaders': [
            {
                'categoryName': 'Rushing',
                'source': 'rushing',
                'headers': [
                    {'key': 'att', 'label': 'Att'},
                    {'key': 'yds', 'label': 'Yds'},
                    {'key': 'avg', 'label': 'Avg'},
                    {'key': 'td', 'label': 'TD'}
                ]
            },
            {
                'categoryName': 'Passing',
                'source': 'passing',
                'headers': [
                    {'key': 'comp', 'label': 'Comp'},
                    {'key': 'att', 'label': 'Att'},
                    {'key': 'pct', 'label': 'Pct'},
                    {'key': 'yds', 'label': 'Yds'},
                    {'key': 'td', 'label': 'TD'}
                ]
            },
            {
                'categoryName': 'Receiving',
                'source': 'receiving',
                'headers': [
                    {'key': 'rec', 'label': 'Rec'},
                    {'key': 'yds', 'label': 'Yds'},
                    {'key': 'td', 'label': 'TD'}
                ]
            }
        ]
    },
    'boys-soccer': {
        'name': 'Boys Soccer',
        'file': 'boys_soccer_data.json',
        'standings_file': 'boys_soccer_standings.json',
        'standings_type': 'cmc',  # Central Maryland Conference with divisions
        'leaders': [
            {
                'categoryName': 'Scoring',
                'source': 'scoring',
                'headers': [
                    {'key': 'gp', 'label': 'GP'},
                    {'key': 'g', 'label': 'G'},
                    {'key': 'a', 'label': 'A'},
                    {'key': 'pts', 'label': 'Pts'}
                ]
            },
            {
                'categoryName': 'Goalkeepers',
                'source': 'goalkeepers',
                'headers': [
                    {'key': 'gp', 'label': 'GP'},
                    {'key': 'ga', 'label': 'GA'},
                    {'key': 'so', 'label': 'SO'},
                    {'key': 'gaa', 'label': 'GAA'}
                ]
            }
        ]
    },
    'girls-soccer': {
        'name': 'Girls Soccer',
        'file': 'girls_soccer_data.json',
        'standings_file': 'girls_soccer_standings.json',
        'standings_type': 'cmc',
        'leaders': [
            {
                'categoryName': 'Scoring',
                'source': 'scoring',
                'headers': [
                    {'key': 'gp', 'label': 'GP'},
                    {'key': 'g', 'label': 'G'},
                    {'key': 'a', 'label': 'A'},
                    {'key': 'pts', 'label': 'Pts'}
                ]
            },
            {
                'categoryName': 'Goalkeepers',
                'source': 'goalkeepers',
                'headers': [
                    {'key': 'gp', 'label': 'GP'},
                    {'key': 'ga', 'label': 'GA'},
                    {'key': 'so', 'label': 'SO'},
                    {'key': 'gaa', 'label': 'GAA'}
                ]
            }
        ]
    },
    'field-hockey': {
        'name': 'Field Hockey',
        'file': 'field_hockey_data.json',
        'standings_file': 'field_hockey_standings.json',
        'standings_type': 'cmc',
        'leaders': [
            {
                'categoryName': 'Scoring',
                'source': 'scoring',
                'headers': [
                    {'key': 'gp', 'label': 'GP'},
                    {'key': 'g', 'label': 'G'},
                    {'key': 'a', 'label': 'A'},
                    {'key': 'pts', 'label': 'Pts'}
                ]
            },
            {
                'categoryName': 'Goalkeepers',
                'source': 'goalkeepers',
                'headers': [
                    {'key': 'gp', 'label': 'GP'},
                    {'key': 'ga', 'label': 'GA'},
                    {'key': 'so', 'label': 'SO'},
                    {'key': 'gaa', 'label': 'GAA'}
                ]
            }
        ]
    },
    'volleyball': {
        'name': 'Volleyball',
        'file': 'volleyball_data.json',
        'standings_file': 'volleyball_standings.json',
        'standings_type': 'cmc',
        'leaders': [
            {
                'categoryName': 'Kills',
                'source': 'kills',
                'headers': [
                    {'key': 'sp', 'label': 'SP'},
                    {'key': 'kills', 'label': 'Kills'},
                    {'key': 'avg', 'label': 'Avg'}
                ]
            },
            {
                'categoryName': 'Assists',
                'source': 'assists',
                'headers': [
                    {'key': 'sp', 'label': 'SP'},
                    {'key': 'assists', 'label': 'Asts'},
                    {'key': 'avg', 'label': 'Avg'}
                ]
            },
            {
                'categoryName': 'Digs',
                'source': 'digs',
                'headers': [
                    {'key': 'sp', 'label': 'SP'},
                    {'key': 'digs', 'label': 'Digs'},
                    {'key': 'avg', 'label': 'Avg'}
                ]
            }
        ]
    },
    'cross-country': {
        'name': 'Cross Country',
        'file': 'cross_country_data.json',
        'leaders': [
            {
                'categoryName': 'Boys Top Times',
                'source': 'boys',
                'headers': [
                    {'key': 'time', 'label': 'Time'}
                ]
            },
            {
                'categoryName': 'Girls Top Times',
                'source': 'girls',
                'headers': [
                    {'key': 'time', 'label': 'Time'}
                ]
            }
        ]
    },
    'golf': {
        'name': 'Golf',
        'file': 'golf_data.json',
        'leaders': [
            {
                'categoryName': '9-Hole Average',
                'source': 'players',
                'headers': [
                    {'key': 'average', 'label': 'Avg'}
                ]
            }
        ]
    },
    'boys-basketball': {
        'name': 'Boys Basketball',
        'file': 'boys_basketball_data.json',
        'standings_file': 'boys_basketball_standings.json',
        'standings_type': 'cmc_basketball',
        'leaders': [
            {
                'categoryName': 'Scoring',
                'source': 'scoring',
                'headers': [
                    {'key': 'gp', 'label': 'GP'},
                    {'key': 'pts', 'label': 'Pts'},
                    {'key': 'avg', 'label': 'Avg'}
                ]
            },
            {
                'categoryName': 'Rebounds',
                'source': 'rebounds',
                'headers': [
                    {'key': 'gp', 'label': 'GP'},
                    {'key': 'reb', 'label': 'Reb'},
                    {'key': 'avg', 'label': 'Avg'}
                ]
            },
            {
                'categoryName': 'Assists',
                'source': 'assists',
                'headers': [
                    {'key': 'gp', 'label': 'GP'},
                    {'key': 'ast', 'label': 'Ast'},
                    {'key': 'avg', 'label': 'Avg'}
                ]
            }
        ]
    },
    'girls-basketball': {
        'name': 'Girls Basketball',
        'file': 'girls_basketball_data.json',
        'standings_file': 'girls_basketball_standings.json',
        'standings_type': 'cmc_basketball',
        'leaders': [
            {
                'categoryName': 'Scoring',
                'source': 'scoring',
                'headers': [
                    {'key': 'gp', 'label': 'GP'},
                    {'key': 'pts', 'label': 'Pts'},
                    {'key': 'avg', 'label': 'Avg'}
                ]
            },
            {
                'categoryName': 'Rebounds',
                'source': 'rebounds',
                'headers': [
                    {'key': 'gp', 'label': 'GP'},
                    {'key': 'reb', 'label': 'Reb'},
                    {'key': 'avg', 'label': 'Avg'}
                ]
            },
            {
                'categoryName': 'Assists',
                'source': 'assists',
                'headers': [
                    {'key': 'gp', 'label': 'GP'},
                    {'key': 'ast', 'label': 'Ast'},
                    {'key': 'avg', 'label': 'Avg'}
                ]
            }
        ]
    },
    'boys-wrestling': {
        'name': 'Boys Wrestling',
        'file': 'boys_wrestling_data.json',
        'leaders_from_keys': True,
        'leader_headers': [
            {'key': 'rank', 'label': 'Rank'},
        ],
        'leaders': []
    },
    'girls-wrestling': {
        'name': 'Girls Wrestling',
        'file': 'girls_wrestling_data.json',
        'leaders_from_keys': True,
        'leader_headers': [
            {'key': 'rank', 'label': 'Rank'},
        ],
        'leaders': []
    },
    'indoor-track': {
        'name': 'Indoor Track & Field',
        'file': 'indoor_track_data.json',
        'leaders_from_keys': True,
        'leader_headers': [
            {'key': 'result', 'label': 'Result'},
        ],
        'leaders': []
    },
    'swimming': {
        'name': 'Swimming & Diving',
        'file': 'swimming_data.json',
        'leaders_from_keys': True,
        'leader_headers': [
            {'key': 'result', 'label': 'Result'},
        ],
        'leaders': []
    }
}

# Rankings by date (hardcoded since they're not in JSON)
RANKINGS_BY_DATE = {
    '2025_10_23': [
        {'sport': 'Football', 'items': [{'team': 'Linganore'}, {'team': 'Oakdale'}, {'team': 'Middletown'}, {'team': 'Urbana'}]},
        {'sport': 'Boys Soccer', 'items': [{'team': 'Tuscarora'}, {'team': 'Urbana'}, {'team': 'Linganore'}, {'team': 'Brunswick'}]},
        {'sport': 'Girls Flag Football', 'items': [{'team': 'Urbana'}, {'team': 'Linganore'}, {'team': 'Frederick'}, {'team': 'Thomas Johnson'}]},
        {'sport': 'Girls Soccer', 'items': [{'team': 'Oakdale'}, {'team': 'Linganore'}, {'team': 'Brunswick'}, {'team': 'Middletown'}]},
        {'sport': 'Volleyball', 'items': [{'team': 'Urbana'}, {'team': 'Tuscarora'}, {'team': 'Oakdale'}, {'team': 'Maryland School for the Deaf'}]},
        {'sport': 'Field Hockey', 'items': [{'team': 'Linganore'}, {'team': 'Urbana'}, {'team': 'Walkersville'}, {'team': 'Oakdale'}]},
        {'sport': 'Boys Cross Country', 'items': [{'team': 'Urbana'}, {'team': 'Thomas Johnson'}, {'team': 'Brunswick'}, {'team': 'Oakdale'}]},
        {'sport': 'Girls Cross Country', 'items': [{'team': 'Urbana'}, {'team': 'Thomas Johnson'}, {'team': 'Frederick'}, {'team': 'Tuscarora'}]},
        {'sport': 'Golf', 'items': [{'team': 'Linganore'}, {'team': 'Middletown'}, {'team': 'Oakdale'}]},
    ],
    '2025_12_06': [
        {'sport': 'Football', 'items': [{'team': 'Linganore'}, {'team': 'Oakdale'}, {'team': 'Middletown'}, {'team': 'Urbana'}]},
        {'sport': 'Boys Soccer', 'items': [{'team': 'Tuscarora'}, {'team': 'Urbana'}, {'team': 'Linganore'}, {'team': 'Brunswick'}]},
        {'sport': 'Girls Flag Football', 'items': [{'team': 'Urbana'}, {'team': 'Linganore'}, {'team': 'Frederick'}, {'team': 'Thomas Johnson'}]},
        {'sport': 'Girls Soccer', 'items': [{'team': 'Oakdale'}, {'team': 'Linganore'}, {'team': 'Brunswick'}, {'team': 'Middletown'}]},
        {'sport': 'Volleyball', 'items': [{'team': 'Urbana'}, {'team': 'Tuscarora'}, {'team': 'Oakdale'}, {'team': 'Maryland School for the Deaf'}]},
        {'sport': 'Field Hockey', 'items': [{'team': 'Linganore'}, {'team': 'Urbana'}, {'team': 'Walkersville'}, {'team': 'Oakdale'}]},
        {'sport': 'Boys Cross Country', 'items': [{'team': 'Urbana'}, {'team': 'Thomas Johnson'}, {'team': 'Brunswick'}, {'team': 'Oakdale'}]},
        {'sport': 'Girls Cross Country', 'items': [{'team': 'Urbana'}, {'team': 'Thomas Johnson'}, {'team': 'Frederick'}, {'team': 'Tuscarora'}]},
        {'sport': 'Golf', 'items': [{'team': 'Linganore'}, {'team': 'Middletown'}, {'team': 'Oakdale'}]},
    ],
    '2026_01_29': [
        {'sport': 'Boys Basketball', 'items': [{'team': 'Middletown'}, {'team': 'Oakdale'}, {'team': 'Linganore'}, {'team': 'T. Johnson'}]},
        {'sport': 'Girls Basketball', 'items': [{'team': 'Linganore'}, {'team': 'Urbana'}, {'team': 'Frederick'}, {'team': 'Oakdale'}]},
        {'sport': 'Boys Wrestling', 'items': [{'team': 'Middletown'}, {'team': 'Brunswick'}, {'team': 'Oakdale'}]},
        {'sport': 'Girls Wrestling', 'items': [{'team': 'Tuscarora'}, {'team': 'Urbana'}, {'team': 'Frederick'}]},
        {'sport': 'Boys Indoor Track & Field', 'items': [{'team': 'Urbana'}, {'team': 'Oakdale'}, {'team': 'Linganore'}, {'team': 'Thomas Johnson'}]},
        {'sport': 'Girls Indoor Track & Field', 'items': [{'team': 'Urbana'}, {'team': 'Thomas Johnson'}, {'team': 'Frederick'}, {'team': 'Oakdale'}]},
    ]
}


def format_key_as_category(key: str) -> str:
    """Convert a JSON key like 'wc_106' or 'boys_55_meter_dash' to a display name."""
    import re as _re
    # Wrestling weight classes: wc_106 -> "106 lbs"
    if key.startswith('wc_'):
        return f"{key[3:]} lbs"
    # Track/swim events: boys_55_meter_dash -> "Boys: 55-meter dash"
    for prefix in ['boys_', 'girls_']:
        if key.startswith(prefix):
            gender = prefix.rstrip('_').capitalize()
            event = key[len(prefix):].replace('_', ' ')
            # Fix "55 meter dash" -> "55-meter dash", "55 meter hurdles" -> "55-meter hurdles"
            event = _re.sub(r'(\d+) meter (dash|hurdles)', r'\1-meter \2', event)
            # Fix "1600 meters" -> "1,600 meters", "3200 meters" -> "3,200 meters"
            event = _re.sub(r'^(\d)(\d{3})\b', r'\1,\2', event)
            event = event[0].upper() + event[1:] if event else event
            return f"{gender}: {event}"
    return key.replace('_', ' ').title()


def load_json_data(date_str: str, filename: str) -> dict:
    """Load JSON data from a file."""
    filepath = DATA_DIR / date_str / filename
    if filepath.exists():
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}


def build_sport_data(sport_id: str, config: dict, date_str: str) -> dict:
    """Build sport data structure for a single date."""
    data = load_json_data(date_str, config['file'])
    if not data:
        return None

    leaders = []
    if config.get('leaders_from_keys'):
        # Dynamic categories from JSON keys (wrestling weight classes, track/swim events)
        leader_headers = config.get('leader_headers', [])
        for key, players in data.items():
            if players:
                leaders.append({
                    'categoryName': format_key_as_category(key),
                    'headers': leader_headers,
                    'players': players
                })
    else:
        for leader_config in config['leaders']:
            source_key = leader_config['source']

            # Handle different data structures
            if source_key == 'players':
                # Golf has flat list
                players = data if isinstance(data, list) else []
            else:
                players = data.get(source_key, [])

            if players:
                leaders.append({
                    'categoryName': leader_config['categoryName'],
                    'headers': leader_config['headers'],
                    'players': players  # Show all players
                })

    # Load standings if available
    standings = []
    standings_file = config.get('standings_file')
    standings_type = config.get('standings_type')

    if standings_file:
        standings_data = load_json_data(date_str, standings_file)
        if standings_data:
            if standings_type == 'fcps':
                # FCPS conference format: {fcps: [{team, wins, losses, pf, pa}], other_schools: [{team, wins, losses, pf, pa}]}
                fcps_teams = standings_data.get('fcps', [])
                if fcps_teams:
                    standings.append({
                        'division': 'FCPS',
                        'headers': [
                            {'key': 'wins', 'label': 'W'},
                            {'key': 'losses', 'label': 'L'},
                            {'key': 'pf', 'label': 'PF'},
                            {'key': 'pa', 'label': 'PA'}
                        ],
                        'teams': fcps_teams
                    })
                # Add OTHER SCHOOLS if present (for Football)
                other_schools = standings_data.get('other_schools', [])
                if other_schools:
                    standings.append({
                        'division': 'Other Schools',
                        'headers': [
                            {'key': 'wins', 'label': 'W'},
                            {'key': 'losses', 'label': 'L'},
                            {'key': 'pf', 'label': 'PF'},
                            {'key': 'pa', 'label': 'PA'}
                        ],
                        'teams': other_schools
                    })
            elif standings_type == 'cmc_basketball':
                # Basketball CMC format: {DIVISION: [{team, div_w, div_l, overall_w, overall_l}]}
                for division, teams in standings_data.items():
                    if teams:
                        standings.append({
                            'division': division,
                            'headers': [
                                {'key': 'div_w', 'label': 'Div W'},
                                {'key': 'div_l', 'label': 'Div L'},
                                {'key': 'overall_w', 'label': 'Ovr W'},
                                {'key': 'overall_l', 'label': 'Ovr L'}
                            ],
                            'teams': teams
                        })
            elif standings_type == 'cmc':
                # Central Maryland Conference format: {DIVISION: [{team, div_wins, div_losses, div_ties, overall_wins, overall_losses, overall_ties}]}
                for division, teams in standings_data.items():
                    if teams:
                        standings.append({
                            'division': division,
                            'headers': [
                                {'key': 'div_wins', 'label': 'Div W'},
                                {'key': 'div_losses', 'label': 'Div L'},
                                {'key': 'div_ties', 'label': 'Div T'},
                                {'key': 'overall_wins', 'label': 'Ovr W'},
                                {'key': 'overall_losses', 'label': 'Ovr L'},
                                {'key': 'overall_ties', 'label': 'Ovr T'}
                            ],
                            'teams': teams
                        })

    return {
        'id': sport_id,
        'name': config['name'],
        'date': date_str,
        'standings': standings,
        'leaders': leaders
    }


def generate_data_js():
    """Generate the data.js file."""
    all_sports_data = []

    # Build sports data for each date
    for date_config in DATES:
        date_str = date_config['value']
        for sport_id, config in SPORTS_CONFIG.items():
            sport_data = build_sport_data(sport_id, config, date_str)
            if sport_data:
                all_sports_data.append(sport_data)

    # Build rankings data
    rankings_data = []
    for date_config in DATES:
        date_str = date_config['value']
        rankings_data.append({
            'date': date_str,
            'items': RANKINGS_BY_DATE.get(date_str, [])
        })

    # Generate JavaScript
    js_content = f"""// Auto-generated data file
// Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

export const availableDates = {json.dumps(DATES, indent=2)};

export const rankings = {json.dumps(rankings_data, indent=2)};

export const sportsData = {json.dumps(all_sports_data, indent=2)};
"""

    # Write to file
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(js_content)

    print(f"Generated {OUTPUT_FILE}")
    print(f"  - {len(DATES)} dates")
    print(f"  - {len(all_sports_data)} sport entries")

    # Also regenerate embed HTML files
    print("\nRegenerating embed HTML files...")
    generate_all_embeds()


if __name__ == '__main__':
    generate_data_js()
