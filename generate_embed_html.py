#!/usr/bin/env python3
"""
Generate embeddable HTML snippets for CMS use.

This script generates standalone HTML snippets for each sport that can be
copied and pasted directly into a CMS content editor. The snippets include
inline styles and are self-contained with no external dependencies.

Usage:
    python generate_embed_html.py [--date YYYY_MM_DD] [--sport SPORT]

Output:
    docs/embed/ folder with HTML snippets for each sport
"""

import argparse
import json
import os
from pathlib import Path

# Inline CSS styles for the embeddable HTML
EMBED_STYLES = """
<style>
.hs-hangout-embed {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #1a1a1a;
    line-height: 1.5;
    max-width: 100%;
}
.hs-hangout-embed h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1e3a5f;
    margin: 0 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e5e5e5;
}
.hs-hangout-embed h3 {
    font-size: 1.125rem;
    font-weight: 700;
    color: #333;
    margin: 1.5rem 0 0.75rem 0;
}
.hs-hangout-embed h4 {
    font-size: 0.875rem;
    font-weight: 700;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 0.5rem 0;
}
.hs-hangout-embed .standings-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}
.hs-hangout-embed .leaders-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
}
.hs-hangout-embed .stats-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
    margin-bottom: 1rem;
    border: 1px solid #e5e5e5;
}
.hs-hangout-embed .stats-table th {
    background-color: #f5f5f5;
    padding: 0.5rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    color: #666;
    border-bottom: 2px solid #ddd;
}
.hs-hangout-embed .stats-table th.numeric {
    text-align: center;
}
.hs-hangout-embed .stats-table td {
    padding: 0.5rem;
    border-bottom: 1px solid #eee;
}
.hs-hangout-embed .stats-table td.numeric {
    text-align: center;
    font-family: 'SF Mono', Monaco, 'Courier New', monospace;
}
.hs-hangout-embed .stats-table tr:nth-child(even) {
    background-color: #fafafa;
}
.hs-hangout-embed .stats-table tr:hover {
    background-color: #f0f7ff;
}
.hs-hangout-embed .player-name {
    font-weight: 500;
}
.hs-hangout-embed .player-school {
    font-size: 0.75rem;
    color: #666;
}
.hs-hangout-embed .leader-card {
    border: 1px solid #e5e5e5;
    border-radius: 4px;
    overflow: hidden;
}
.hs-hangout-embed .leader-card-header {
    background-color: #f5f5f5;
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid #e5e5e5;
}
.hs-hangout-embed .leader-card-header h4 {
    margin: 0;
}
</style>
"""


def load_json_data(date_str: str, filename: str) -> dict:
    """Load JSON data from the data folder."""
    filepath = Path(f'data/{date_str}/{filename}')
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return None


def generate_standings_html(standings_data: dict, standings_type: str) -> str:
    """Generate HTML for standings tables."""
    if not standings_data:
        return ""

    html = '<div class="standings-grid">\n'

    if standings_type == 'fcps':
        # FCPS standings
        fcps_teams = standings_data.get('fcps', [])
        if fcps_teams:
            html += '<div>\n'
            html += '<h4>FCPS</h4>\n'
            html += '<table class="stats-table">\n'
            html += '<thead><tr><th>Team</th><th class="numeric">W</th><th class="numeric">L</th><th class="numeric">PF</th><th class="numeric">PA</th></tr></thead>\n'
            html += '<tbody>\n'
            for team in fcps_teams:
                html += f'<tr><td>{team.get("team", "")}</td>'
                html += f'<td class="numeric">{team.get("wins", "")}</td>'
                html += f'<td class="numeric">{team.get("losses", "")}</td>'
                html += f'<td class="numeric">{team.get("pf", "")}</td>'
                html += f'<td class="numeric">{team.get("pa", "")}</td></tr>\n'
            html += '</tbody></table>\n</div>\n'

        # Other Schools
        other_schools = standings_data.get('other_schools', [])
        if other_schools:
            html += '<div>\n'
            html += '<h4>Other Schools</h4>\n'
            html += '<table class="stats-table">\n'
            html += '<thead><tr><th>Team</th><th class="numeric">W</th><th class="numeric">L</th><th class="numeric">PF</th><th class="numeric">PA</th></tr></thead>\n'
            html += '<tbody>\n'
            for team in other_schools:
                html += f'<tr><td>{team.get("team", "")}</td>'
                html += f'<td class="numeric">{team.get("wins", "")}</td>'
                html += f'<td class="numeric">{team.get("losses", "")}</td>'
                html += f'<td class="numeric">{team.get("pf", "-")}</td>'
                html += f'<td class="numeric">{team.get("pa", "-")}</td></tr>\n'
            html += '</tbody></table>\n</div>\n'

    elif standings_type == 'cmc':
        # CMC standings with divisions
        for division, teams in standings_data.items():
            if not teams:
                continue
            html += '<div>\n'
            html += f'<h4>{division}</h4>\n'
            html += '<table class="stats-table">\n'
            html += '<thead><tr><th>Team</th><th class="numeric">Div W</th><th class="numeric">Div L</th><th class="numeric">Div T</th>'
            html += '<th class="numeric">Ovr W</th><th class="numeric">Ovr L</th><th class="numeric">Ovr T</th></tr></thead>\n'
            html += '<tbody>\n'
            for team in teams:
                html += f'<tr><td>{team.get("team", "")}</td>'
                html += f'<td class="numeric">{team.get("div_wins", "")}</td>'
                html += f'<td class="numeric">{team.get("div_losses", "")}</td>'
                html += f'<td class="numeric">{team.get("div_ties", "0")}</td>'
                html += f'<td class="numeric">{team.get("overall_wins", "")}</td>'
                html += f'<td class="numeric">{team.get("overall_losses", "")}</td>'
                html += f'<td class="numeric">{team.get("overall_ties", "0")}</td></tr>\n'
            html += '</tbody></table>\n</div>\n'

    html += '</div>\n'
    return html


def generate_leaders_html(stats_data: dict, leader_configs: list) -> str:
    """Generate HTML for stat leader tables."""
    if not stats_data:
        return ""

    html = '<div class="leaders-grid">\n'

    for config in leader_configs:
        source = config.get('source', '')
        players = stats_data.get(source, [])
        if not players:
            continue

        html += '<div class="leader-card">\n'
        html += f'<div class="leader-card-header"><h4>{config["categoryName"]}</h4></div>\n'
        html += '<table class="stats-table">\n'
        html += '<thead><tr><th>Player</th>'
        for header in config['headers']:
            html += f'<th class="numeric">{header["label"]}</th>'
        html += '</tr></thead>\n'
        html += '<tbody>\n'

        for player in players:
            html += '<tr>'
            html += f'<td><div class="player-name">{player.get("player", "")}</div>'
            html += f'<div class="player-school">{player.get("school", "")}</div></td>'
            for header in config['headers']:
                value = player.get(header['key'], '')
                html += f'<td class="numeric">{value}</td>'
            html += '</tr>\n'

        html += '</tbody></table>\n</div>\n'

    html += '</div>\n'
    return html


# Sport configurations
SPORT_CONFIGS = {
    'football': {
        'name': 'Football',
        'data_file': 'football_data.json',
        'standings_file': 'football_standings.json',
        'standings_type': 'fcps',
        'leaders': [
            {'categoryName': 'Rushing', 'source': 'rushing', 'headers': [
                {'key': 'att', 'label': 'Att'}, {'key': 'yds', 'label': 'Yds'},
                {'key': 'avg', 'label': 'Avg'}, {'key': 'td', 'label': 'TD'}
            ]},
            {'categoryName': 'Passing', 'source': 'passing', 'headers': [
                {'key': 'comp', 'label': 'Cmp'}, {'key': 'att', 'label': 'Att'},
                {'key': 'pct', 'label': 'Pct'}, {'key': 'yds', 'label': 'Yds'}, {'key': 'td', 'label': 'TD'}
            ]},
            {'categoryName': 'Receiving', 'source': 'receiving', 'headers': [
                {'key': 'rec', 'label': 'Rec'}, {'key': 'yds', 'label': 'Yds'},
                {'key': 'avg', 'label': 'Avg'}, {'key': 'td', 'label': 'TD'}
            ]}
        ]
    },
    'girls_flag_football': {
        'name': 'Girls Flag Football',
        'data_file': 'girls_flag_football_data.json',
        'standings_file': 'girls_flag_football_standings.json',
        'standings_type': 'fcps',
        'leaders': [
            {'categoryName': 'Rushing', 'source': 'rushing', 'headers': [
                {'key': 'att', 'label': 'Att'}, {'key': 'yds', 'label': 'Yds'},
                {'key': 'avg', 'label': 'Avg'}, {'key': 'td', 'label': 'TD'}
            ]},
            {'categoryName': 'Passing', 'source': 'passing', 'headers': [
                {'key': 'comp', 'label': 'Cmp'}, {'key': 'att', 'label': 'Att'},
                {'key': 'pct', 'label': 'Pct'}, {'key': 'yds', 'label': 'Yds'}, {'key': 'td', 'label': 'TD'}
            ]},
            {'categoryName': 'Receiving', 'source': 'receiving', 'headers': [
                {'key': 'rec', 'label': 'Rec'}, {'key': 'yds', 'label': 'Yds'},
                {'key': 'avg', 'label': 'Avg'}, {'key': 'td', 'label': 'TD'}
            ]}
        ]
    },
    'boys_soccer': {
        'name': 'Boys Soccer',
        'data_file': 'boys_soccer_data.json',
        'standings_file': 'boys_soccer_standings.json',
        'standings_type': 'cmc',
        'leaders': [
            {'categoryName': 'Scoring Leaders', 'source': 'scoring', 'headers': [
                {'key': 'gp', 'label': 'GP'}, {'key': 'g', 'label': 'G'},
                {'key': 'a', 'label': 'A'}, {'key': 'pts', 'label': 'Pts'}
            ]},
            {'categoryName': 'Goalkeepers', 'source': 'goalkeepers', 'headers': [
                {'key': 'gp', 'label': 'GP'}, {'key': 'saves', 'label': 'Sv'},
                {'key': 'ga', 'label': 'GA'}, {'key': 'sv_pct', 'label': 'Sv%'}, {'key': 'gaa', 'label': 'GAA'}
            ]}
        ]
    },
    'girls_soccer': {
        'name': 'Girls Soccer',
        'data_file': 'girls_soccer_data.json',
        'standings_file': 'girls_soccer_standings.json',
        'standings_type': 'cmc',
        'leaders': [
            {'categoryName': 'Scoring Leaders', 'source': 'scoring', 'headers': [
                {'key': 'gp', 'label': 'GP'}, {'key': 'g', 'label': 'G'},
                {'key': 'a', 'label': 'A'}, {'key': 'pts', 'label': 'Pts'}
            ]},
            {'categoryName': 'Goalkeepers', 'source': 'goalkeepers', 'headers': [
                {'key': 'gp', 'label': 'GP'}, {'key': 'saves', 'label': 'Sv'},
                {'key': 'ga', 'label': 'GA'}, {'key': 'sv_pct', 'label': 'Sv%'}, {'key': 'gaa', 'label': 'GAA'}
            ]}
        ]
    },
    'volleyball': {
        'name': 'Volleyball',
        'data_file': 'volleyball_data.json',
        'standings_file': 'volleyball_standings.json',
        'standings_type': 'cmc',
        'leaders': [
            {'categoryName': 'Kills', 'source': 'kills', 'headers': [
                {'key': 'sp', 'label': 'SP'}, {'key': 'kills', 'label': 'Kills'},
                {'key': 'avg', 'label': 'Avg'}
            ]},
            {'categoryName': 'Assists', 'source': 'assists', 'headers': [
                {'key': 'sp', 'label': 'SP'}, {'key': 'assists', 'label': 'Ast'},
                {'key': 'avg', 'label': 'Avg'}
            ]},
            {'categoryName': 'Digs', 'source': 'digs', 'headers': [
                {'key': 'sp', 'label': 'SP'}, {'key': 'digs', 'label': 'Digs'},
                {'key': 'avg', 'label': 'Avg'}
            ]}
        ]
    },
    'field_hockey': {
        'name': 'Field Hockey',
        'data_file': 'field_hockey_data.json',
        'standings_file': 'field_hockey_standings.json',
        'standings_type': 'cmc',
        'leaders': [
            {'categoryName': 'Scoring Leaders', 'source': 'scoring', 'headers': [
                {'key': 'gp', 'label': 'GP'}, {'key': 'g', 'label': 'G'},
                {'key': 'a', 'label': 'A'}, {'key': 'pts', 'label': 'Pts'}
            ]},
            {'categoryName': 'Goalkeepers', 'source': 'goalkeepers', 'headers': [
                {'key': 'gp', 'label': 'GP'}, {'key': 'saves', 'label': 'Sv'},
                {'key': 'ga', 'label': 'GA'}, {'key': 'sv_pct', 'label': 'Sv%'}, {'key': 'gaa', 'label': 'GAA'}
            ]}
        ]
    },
    'cross_country': {
        'name': 'Cross Country',
        'data_file': 'cross_country_data.json',
        'standings_file': None,
        'standings_type': None,
        'leaders': [
            {'categoryName': 'Boys Top 5K Times', 'source': 'boys', 'headers': [
                {'key': 'time', 'label': 'Time'}
            ]},
            {'categoryName': 'Girls Top 5K Times', 'source': 'girls', 'headers': [
                {'key': 'time', 'label': 'Time'}
            ]}
        ]
    },
    'golf': {
        'name': 'Golf',
        'data_file': 'golf_data.json',
        'standings_file': None,
        'standings_type': None,
        'leaders': [
            {'categoryName': '9-Hole Average', 'source': 'players', 'headers': [
                {'key': 'average', 'label': 'Avg'}
            ]}
        ]
    }
}

AVAILABLE_DATES = ['2025_10_23', '2025_12_06']


def generate_embed_for_sport(sport_id: str, config: dict, date_str: str) -> str:
    """Generate embeddable HTML for a single sport."""

    # Load data
    stats_data = load_json_data(date_str, config['data_file'])
    standings_data = None
    if config.get('standings_file'):
        standings_data = load_json_data(date_str, config['standings_file'])

    # Build HTML
    html = EMBED_STYLES
    html += f'<div class="hs-hangout-embed">\n'
    html += f'<h2>{config["name"]}</h2>\n'

    # Standings section
    if standings_data:
        html += '<h3>Standings</h3>\n'
        html += generate_standings_html(standings_data, config['standings_type'])

    # Leaders section
    if stats_data:
        html += '<h3>Individual Leaders</h3>\n'

        # Handle golf which has flat list
        if sport_id == 'golf' and isinstance(stats_data, list):
            stats_data = {'players': stats_data}

        html += generate_leaders_html(stats_data, config['leaders'])

    html += '</div>\n'
    return html


def main():
    parser = argparse.ArgumentParser(description='Generate embeddable HTML for CMS')
    parser.add_argument('--date', type=str, help='Date (YYYY_MM_DD)')
    parser.add_argument('--sport', type=str, help='Sport ID (e.g., football, boys_soccer)')
    args = parser.parse_args()

    # Create output directory
    embed_dir = Path('docs/embed')
    embed_dir.mkdir(exist_ok=True)

    # Determine which dates and sports to process
    dates = [args.date] if args.date else AVAILABLE_DATES
    sports = [args.sport] if args.sport else list(SPORT_CONFIGS.keys())

    for date_str in dates:
        date_dir = embed_dir / date_str
        date_dir.mkdir(exist_ok=True)

        for sport_id in sports:
            if sport_id not in SPORT_CONFIGS:
                print(f"Warning: Unknown sport '{sport_id}'")
                continue

            config = SPORT_CONFIGS[sport_id]

            # Check if data exists
            data_path = Path(f'data/{date_str}/{config["data_file"]}')
            if not data_path.exists():
                continue

            # Generate embed HTML
            html = generate_embed_for_sport(sport_id, config, date_str)

            # Save to file
            output_file = date_dir / f'{sport_id}.html'
            with open(output_file, 'w') as f:
                f.write(html)
            print(f"✓ Generated {output_file}")

    print(f"\nEmbed files saved to {embed_dir}/")
    print("Copy the contents of any .html file to paste into your CMS.")


if __name__ == '__main__':
    main()
