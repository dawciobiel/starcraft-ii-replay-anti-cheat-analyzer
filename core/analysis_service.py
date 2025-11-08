# core/analysis_service.py

import os
import datetime
import configparser
import sqlite3
import json
import sys

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser.parser_v1_1 import parse_replay
from analyzer.analyzer import analyze_replay

def run_full_analysis(replay_path):
    """
    Runs the full analysis pipeline for a given replay file.
    
    Args:
        replay_path: The absolute path to the .SC2Replay file.
        
    Returns:
        A dictionary containing the analysis results.
    """
    
    # --- Setup Paths and Config ---
    replay_base_name = os.path.splitext(os.path.basename(replay_path))[0]
    base_analysis_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', "replays-analysis")

    config = configparser.ConfigParser(interpolation=None)
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config', 'config.ini'))
    timestamp_format = config.get('Analyzer', 'TimestampFormat', fallback='%Y-%m-%d_%H-%M-%S')
    
    timestamp = datetime.datetime.now().strftime(timestamp_format)
    
    current_analysis_dir = os.path.join(base_analysis_dir, replay_base_name, timestamp)
    os.makedirs(current_analysis_dir, exist_ok=True)
    
    parser_db_name = f"{replay_base_name}.parser-v1.1.db"
    db_path = os.path.join(current_analysis_dir, parser_db_name)
    
    # --- Run Parser and Analyzer ---
    parse_replay(replay_path, db_path)
    analyze_replay(db_path, current_analysis_dir)
    
    # --- Collect Results ---
    results = {
        'replay_name': os.path.basename(replay_path),
        'alerts': [],
        'players': [],
        'teams': {}
    }
    
    # Read alerts
    alerts_file_path = os.path.join(current_analysis_dir, 'alerts.json')
    if os.path.exists(alerts_file_path):
        with open(alerts_file_path, 'r') as f:
            results['alerts'] = json.load(f)
            
    # Get Player and Team Info
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    players_data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    results['players'] = players_data
    
    for player in players_data:
        team_id = player['team']
        if team_id not in results['teams']:
            results['teams'][team_id] = []
        results['teams'][team_id].append(player)
        
    # --- Get Player Stats ---
    results['player_stats'] = get_player_stats(db_path)
    results['build_orders'] = get_build_orders(db_path)
    results['charts'] = generate_charts(db_path, current_analysis_dir)
        
    return results

def generate_charts(db_path, output_dir):
    """
    Generates all charts and returns a dictionary of their paths.
    """
    charts = {}
    charts['workers_active'] = generate_workers_active_chart(db_path, output_dir)
    charts['resource_collection_rate'] = generate_resource_collection_rate_chart(db_path, output_dir)
    charts['army_value'] = generate_army_value_chart(db_path, output_dir)
    return charts

# Define unit costs (simplified for common units)
UNIT_COSTS = {
    # Terran
    'SCV': {'minerals': 50, 'vespene': 0},
    'Marine': {'minerals': 50, 'vespene': 0},
    'Marauder': {'minerals': 100, 'vespene': 25},
    'Reaper': {'minerals': 50, 'vespene': 50},
    'Ghost': {'minerals': 150, 'vespene': 125},
    'Hellion': {'minerals': 100, 'vespene': 0},
    'Hellbat': {'minerals': 100, 'vespene': 0},
    'SiegeTank': {'minerals': 150, 'vespene': 125},
    'Thor': {'minerals': 300, 'vespene': 200},
    'Cyclone': {'minerals': 150, 'vespene': 100},
    'Viking': {'minerals': 150, 'vespene': 75},
    'Medivac': {'minerals': 100, 'vespene': 100},
    'Raven': {'minerals': 100, 'vespene': 200},
    'Banshee': {'minerals': 150, 'vespene': 100},
    'Battlecruiser': {'minerals': 400, 'vespene': 300},

    # Zerg
    'Drone': {'minerals': 50, 'vespene': 0},
    'Zergling': {'minerals': 25, 'vespene': 0},
    'Baneling': {'minerals': 25, 'vespene': 25}, # from Zergling
    'Roach': {'minerals': 75, 'vespene': 25},
    'Ravager': {'minerals': 25, 'vespene': 25}, # from Roach
    'Hydralisk': {'minerals': 100, 'vespene': 50},
    'Lurker': {'minerals': 50, 'vespene': 100}, # from Hydralisk
    'Mutalisk': {'minerals': 100, 'vespene': 100},
    'Corruptor': {'minerals': 150, 'vespene': 100},
    'BroodLord': {'minerals': 150, 'vespene': 150}, # from Corruptor
    'Infestor': {'minerals': 100, 'vespene': 150},
    'SwarmHost': {'minerals': 100, 'vespene': 75},
    'Ultralisk': {'minerals': 300, 'vespene': 200},
    'Queen': {'minerals': 150, 'vespene': 0},

    # Protoss
    'Probe': {'minerals': 50, 'vespene': 0},
    'Zealot': {'minerals': 100, 'vespene': 0},
    'Stalker': {'minerals': 125, 'vespene': 50},
    'Sentry': {'minerals': 50, 'vespene': 100},
    'Adept': {'minerals': 100, 'vespene': 25},
    'HighTemplar': {'minerals': 50, 'vespene': 150},
    'DarkTemplar': {'minerals': 125, 'vespene': 125},
    'Immortal': {'minerals': 275, 'vespene': 100},
    'Disruptor': {'minerals': 150, 'vespene': 150},
    'Colossus': {'minerals': 300, 'vespene': 200},
    'Phoenix': {'minerals': 150, 'vespene': 100},
    'VoidRay': {'minerals': 200, 'vespene': 150},
    'Oracle': {'minerals': 150, 'vespene': 150},
    'Tempest': {'minerals': 250, 'vespene': 175},
    'Carrier': {'minerals': 350, 'vespene': 250},
    'Mothership': {'minerals': 300, 'vespene': 300},
}

def generate_army_value_chart(db_path, output_dir):
    """
    Generates a chart of army value over time for all players.
    """
    import matplotlib.pyplot as plt

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    plt.figure(figsize=(10, 6))
    
    cursor.execute("SELECT player_id, name FROM players")
    players = cursor.fetchall()

    max_game_time = 0
    cursor.execute("SELECT MAX(second) FROM timeline")
    max_game_time = cursor.fetchone()[0] or 1 # Avoid division by zero

    for player in players:
        player_id = player['player_id']
        
        # Get all unit born events for the player
        cursor.execute("""
            SELECT t.second, u.name
            FROM units u
            JOIN timeline t ON u.timeline_id = t.timeline_id
            WHERE u.player_id = ?
            ORDER BY t.second
        """, (player_id,))
        unit_born_events = cursor.fetchall()

        # Get all unit died events for the player's units
        cursor.execute("""
            SELECT t.second, ud.unit_name
            FROM unit_deaths ud
            JOIN timeline t ON ud.timeline_id = t.timeline_id
            WHERE ud.player_id = ?
            ORDER BY t.second
        """, (player_id,))
        unit_died_events = cursor.fetchall()

        # Combine and sort all relevant events
        all_events = []
        for event in unit_born_events:
            all_events.append({'second': event['second'], 'type': 'born', 'unit_name': event['name']})
        for event in unit_died_events:
            all_events.append({'second': event['second'], 'type': 'died', 'unit_name': event['unit_name']})
        
        all_events.sort(key=lambda x: x['second'])

        time_points = [0]
        army_values = [0]
        current_army_value = 0

        for event in all_events:
            unit_cost = UNIT_COSTS.get(event['unit_name'], {'minerals': 0, 'vespene': 0})
            total_cost = unit_cost['minerals'] + unit_cost['vespene']

            if event['type'] == 'born':
                current_army_value += total_cost
            elif event['type'] == 'died':
                current_army_value -= total_cost
            
            time_points.append(event['second'])
            army_values.append(current_army_value)
        
        plt.plot(time_points, army_values, label=f"Player {player_id} - {player['name']}")

    conn.close()

    plt.title("Army Value Over Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Army Value (Minerals + Vespene)")
    plt.legend()
    plt.grid(True)
    
    chart_path = os.path.join(output_dir, 'army_value_chart.png')
    plt.savefig(chart_path)
    plt.close()
    
    # Return relative path for web display
    return os.path.join(os.path.basename(os.path.dirname(output_dir)), os.path.basename(output_dir), 'army_value_chart.png')

def generate_resource_collection_rate_chart(db_path, output_dir):
    """
    Generates a chart of resource collection rate over time for all players.
    """
    import matplotlib.pyplot as plt

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    plt.figure(figsize=(10, 6))
    
    cursor.execute("SELECT player_id, name FROM players")
    players = cursor.fetchall()

    for player in players:
        player_id = player['player_id']
        
        cursor.execute("""
            SELECT t.second, p.minerals_collection_rate, p.vespene_collection_rate
            FROM player_stats_events p
            JOIN timeline t ON p.timeline_id = t.timeline_id
            WHERE p.player_id = ?
            ORDER BY t.second
        """, (player_id,))
        
        stats_events = cursor.fetchall()
        
        time_points = [event['second'] for event in stats_events]
        minerals_rate = [event['minerals_collection_rate'] for event in stats_events]
        vespene_rate = [event['vespene_collection_rate'] for event in stats_events]
            
        plt.plot(time_points, minerals_rate, label=f"Player {player_id} - {player['name']} (Minerals)")
        plt.plot(time_points, vespene_rate, label=f"Player {player_id} - {player['name']} (Vespene)", linestyle='--')

    conn.close()

    plt.title("Resource Collection Rate Over Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Collection Rate")
    plt.legend()
    plt.grid(True)
    
    chart_path = os.path.join(output_dir, 'resource_collection_rate_chart.png')
    plt.savefig(chart_path)
    plt.close()
    
    # Return relative path for web display
    return os.path.join(os.path.basename(os.path.dirname(output_dir)), os.path.basename(output_dir), 'resource_collection_rate_chart.png')

def generate_workers_active_chart(db_path, output_dir):
    """
    Generates a chart of active workers over time for all players.
    """
    import matplotlib.pyplot as plt

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    plt.figure(figsize=(10, 6))
    
    cursor.execute("SELECT player_id, name FROM players")
    players = cursor.fetchall()

    for player in players:
        player_id = player['player_id']
        
        cursor.execute("""
            SELECT t.second
            FROM units u
            JOIN timeline t ON u.timeline_id = t.timeline_id
            WHERE u.player_id = ? AND u.name IN ('SCV', 'Probe', 'Drone')
            ORDER BY t.second
        """, (player_id,))
        
        worker_events = cursor.fetchall()
        
        time_points = [0]
        worker_counts = [0]
        current_workers = 0
        
        for event in worker_events:
            current_workers += 1
            time_points.append(event['second'])
            worker_counts.append(current_workers)
            
        plt.plot(time_points, worker_counts, label=f"Player {player_id} - {player['name']}")

    conn.close()

    plt.title("Active Workers Over Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Number of Workers")
    plt.legend()
    plt.grid(True)
    
    chart_path = os.path.join(output_dir, 'workers_active_chart.png')
    plt.savefig(chart_path)
    plt.close()
    
    # Return relative path for web display
    return os.path.join(os.path.basename(os.path.dirname(output_dir)), os.path.basename(output_dir), 'workers_active_chart.png')


def get_build_orders(db_path):
    """
    Retrieves the build order for each player from the database.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    build_orders = {}
    cursor.execute("SELECT player_id, name FROM players")
    players = cursor.fetchall()

    for player in players:
        player_id = player['player_id']
        
        # Get structures built
        cursor.execute("""
            SELECT t.second, s.name as action_name
            FROM structures s
            JOIN timeline t ON s.timeline_id = t.timeline_id
            WHERE s.player_id = ?
        """, (player_id,))
        structures_bo = [{'second': row['second'], 'action': f"Build {row['action_name']}"} for row in cursor.fetchall()]

        # Get units built (excluding workers, as they are counted separately)
        cursor.execute("""
            SELECT t.second, u.name as action_name
            FROM units u
            JOIN timeline t ON u.timeline_id = t.timeline_id
            WHERE u.player_id = ? AND u.name NOT IN ('SCV', 'Probe', 'Drone')
        """, (player_id,))
        units_bo = [{'second': row['second'], 'action': f"Train {row['action_name']}"} for row in cursor.fetchall()]

        # Get upgrades
        cursor.execute("""
            SELECT completed_at as second, name as action_name
            FROM upgrades
            WHERE player_id = ?
        """, (player_id,))
        upgrades_bo = [{'second': row['second'], 'action': f"Research {row['action_name']}"} for row in cursor.fetchall()]

        # Combine and sort all events
        all_events = sorted(structures_bo + units_bo + upgrades_bo, key=lambda x: x['second'])
        build_orders[player_id] = all_events
    
    conn.close()
    return build_orders

def get_player_stats(db_path):
    """
    Retrieves player statistics (APM, EPM) from the database.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    player_stats = {}
    cursor.execute("SELECT player_id, name FROM players")
    players = cursor.fetchall()

    for player in players:
        player_id = player['player_id']
        player_name = player['name']

        # Get average APM and EPM
        cursor.execute("""
            SELECT AVG(apm) as avg_apm, AVG(epm) as avg_epm
            FROM player_apm
            WHERE player_id = ?
        """, (player_id,))
        apm_epm_data = cursor.fetchone()

        player_stats[player_id] = {
            'name': player_name,
            'avg_apm': round(apm_epm_data['avg_apm']) if apm_epm_data['avg_apm'] else 0,
            'avg_epm': round(apm_epm_data['avg_epm']) if apm_epm_data['avg_epm'] else 0,
            'workers_built': 0,
            'structures_built': 0,
            'combat_units_built': 0,
            'enemy_units_destroyed': 0 # Placeholder for now
        }

        # Define combat units for each race (simplified list)
        combat_units = {
            'Terran': ['Marine', 'Marauder', 'Reaper', 'Ghost', 'Hellion', 'Hellbat', 'SiegeTank', 'Thor', 'Cyclone', 'Viking', 'Medivac', 'Raven', 'Banshee', 'Battlecruiser'],
            'Zerg': ['Zergling', 'Baneling', 'Roach', 'Ravager', 'Hydralisk', 'Lurker', 'Mutalisk', 'Corruptor', 'BroodLord', 'Infestor', 'SwarmHost', 'Ultralisk', 'Queen'],
            'Protoss': ['Zealot', 'Stalker', 'Sentry', 'Adept', 'HighTemplar', 'DarkTemplar', 'Immortal', 'Disruptor', 'Colossus', 'Phoenix', 'VoidRay', 'Oracle', 'Tempest', 'Carrier', 'Mothership']
        }
        
        # Get player's race
        cursor.execute("SELECT race FROM players WHERE player_id = ?", (player_id,))
        player_race = cursor.fetchone()[0]

        # Count workers built
        cursor.execute("""
            SELECT COUNT(*) FROM units
            WHERE player_id = ? AND name IN ('SCV', 'Probe', 'Drone')
        """, (player_id,))
        player_stats[player_id]['workers_built'] = cursor.fetchone()[0]

        # Count structures built
        cursor.execute("""
            SELECT COUNT(*) FROM structures
            WHERE player_id = ?
        """, (player_id,))
        player_stats[player_id]['structures_built'] = cursor.fetchone()[0]

        # Count combat units built
        if player_race in combat_units:
            combat_unit_names = combat_units[player_race]
            cursor.execute(f"""
                SELECT COUNT(*) FROM units
                WHERE player_id = ? AND name IN ({','.join(['?' for _ in combat_unit_names])})
            """, (player_id, *combat_unit_names))
            player_stats[player_id]['combat_units_built'] = cursor.fetchone()[0]
    
    conn.close()
    return player_stats
