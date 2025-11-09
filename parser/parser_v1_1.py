# Parser Version: 1.1
import sc2reader
from sc2reader.engine.plugins import APMTracker
import sqlite3
import os

def init_db(db_path):
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    if os.path.exists(db_path):
        os.remove(db_path)
    schema_path = os.path.join(os.path.dirname(__file__), "parser_v1_1_schema.sql")
    with open(schema_path, "r") as f:
        schema = f.read()
    conn = sqlite3.connect(db_path)
    conn.executescript(schema)
    conn.commit()
    return conn

def calculate_epm(replay, player_pid):
    player_events = [e for e in replay.events if hasattr(e, 'player') and e.player.pid == player_pid]

    effective_actions = []
    last_command = None
    last_command_time = -1

    for event in player_events:
        if event.name in ('TargetPointCommandEvent', 'TargetUnitCommandEvent', 'AbilityEvent'):
            is_redundant = (
                last_command and
                event.name == last_command.name and
                event.ability_name == last_command.ability_name and
                event.second - last_command_time < 0.5
            )

            if not is_redundant:
                effective_actions.append(event)
                last_command = event
                last_command_time = event.second

    epm_data = {}
    game_length_minutes = replay.game_length.seconds // 60
    for minute in range(game_length_minutes):
        actions_in_minute = [e for e in effective_actions if minute * 60 <= e.second < (minute + 1) * 60]
        epm = len(actions_in_minute)
        for second in range(minute * 60, (minute + 1) * 60):
            epm_data[second] = epm

    return epm_data

def parse_replay(replay_path, db_path):
    sc2reader.engine.register_plugin(APMTracker())
    replay = sc2reader.load_replay(replay_path, load_level=4)
    conn = init_db(db_path)
    cursor = conn.cursor()

    # Players
    for player in replay.players:
        cursor.execute("""
            INSERT INTO players (player_id, name, toon_id, bnet_url, race, team, color)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (player.pid, player.name, getattr(player, 'toon_id', None), getattr(player, 'url', None), player.play_race, player.team.number, player.color.hex))

    # Timeline
    tick_map = {}
    second_to_timeline_id = {}
    for i, event in enumerate(replay.tracker_events):
        tick = event.frame
        second = event.second
        tick_map[tick] = i + 1
        if second not in second_to_timeline_id:
            second_to_timeline_id[second] = i + 1
        cursor.execute("INSERT INTO timeline (timeline_id, tick, second) VALUES (?, ?, ?)", (i + 1, tick, second))

    # Initial Structures
    initial_main_buildings = set()
    for unit in replay.objects.values():
        if unit.is_building and unit.owner and unit.name in ('CommandCenter', 'Nexus', 'Hatchery') and unit.owner.pid not in initial_main_buildings:
            initial_main_buildings.add(unit.owner.pid)
            cursor.execute("""
                INSERT INTO structures (player_id, name, x, y, z, is_flying, timeline_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                unit.owner.pid,
                unit.name,
                unit.location[0],
                unit.location[1],
                unit.location[2] if len(unit.location) > 2 else None,
                False,  # is_flying
                1 # timeline_id for initial structures
            ))

    # Structures
    for event in replay.tracker_events:
        if event.name in ('UnitBornEvent', 'UnitInitEvent') and event.unit.is_building and event.unit.owner:
            cursor.execute("""
                INSERT INTO structures (player_id, name, x, y, z, is_flying, timeline_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                event.unit.owner.pid,
                event.unit.name,
                event.unit.location[0],
                event.unit.location[1],
                event.unit.location[2] if len(event.unit.location) > 2 else None,
                False,  # is_flying
                tick_map.get(event.frame, 0)
            ))
    # Units
    for event in replay.tracker_events:
        if event.name == "UnitBornEvent" and not event.unit.is_building and event.unit.owner:
            cursor.execute("""
                INSERT INTO units (player_id, name, x, y, z, hp, shield, energy, timeline_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.unit.owner.pid,
                event.unit.name,
                event.unit.location[0],
                event.unit.location[1],
                event.unit.location[2] if len(event.unit.location) > 2 else None,
                getattr(event.unit, "health", None),
                getattr(event.unit, "shield", None),
                getattr(event.unit, "energy", None),
                tick_map.get(event.frame, 0)
            ))

    # Events (Camera, Selection)
    last_camera_positions = {}
    for event in replay.events:
        if event.name == "CameraEvent":
            last_camera_positions[event.player.pid] = (event.x, event.y)
            cursor.execute("""
                INSERT INTO camera_events (player_id, x, y, timeline_id)
                VALUES (?, ?, ?, ?)
            """, (
                event.player.pid,
                event.x,
                event.y,
                tick_map.get(event.frame, 0))
            )

        elif event.name == "SelectionEvent":
            if event.new_units and all(unit.owner != event.player for unit in event.new_units):
                camera_pos = last_camera_positions.get(event.player.pid, (None, None))
                selected_unit_ids = ",".join([str(unit.id) for unit in event.new_units])
                cursor.execute("""
                    INSERT INTO selection_events (player_id, timeline_id, selected_unit_ids, camera_x, camera_y)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    event.player.pid,
                    tick_map.get(event.frame, 0),
                    selected_unit_ids,
                    camera_pos[0],
                    camera_pos[1]
                ))

        elif event.name in ("SetControlGroupEvent", "AddToControlGroupEvent", "GetControlGroupEvent"):
            action_type = None
            if event.name == "SetControlGroupEvent":
                action_type = "set"
            elif event.name == "AddToControlGroupEvent":
                action_type = "add"
            elif event.name == "GetControlGroupEvent":
                action_type = "get"

            if action_type:
                selected_unit_ids = ",".join([str(unit.id) for unit in event.units]) if hasattr(event, 'units') else ""
                cursor.execute("""
                    INSERT INTO control_group_events (player_id, timeline_id, control_group_id, action, units_selected)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    event.player.pid,
                    tick_map.get(event.frame, 0),
                    event.control_group,
                    action_type,
                    selected_unit_ids
                ))
        
        elif event.name == "PlayerStatsEvent":
            cursor.execute("""
                INSERT INTO player_stats_events (player_id, timeline_id, minerals_collection_rate, vespene_collection_rate, workers_active_count, food_used, food_made)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                event.player.pid,
                tick_map.get(event.frame, 0),
                event.minerals_collection_rate,
                event.vespene_collection_rate,
                event.workers_active_count,
                event.food_used,
                event.food_made
            ))
        
        elif event.name == "UnitDiedEvent":
            # Only record if the unit had an owner
            if event.unit.owner:
                killer_player_id = event.killer.pid if event.killer else None
                cursor.execute("""
                    INSERT INTO unit_deaths (unit_id, killer_player_id, player_id, timeline_id, unit_name, x, y)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.unit_id,
                    killer_player_id,
                    event.unit.owner.pid,
                    tick_map.get(event.frame, 0),
                    event.unit.name,
                    event.unit.location[0],
                    event.unit.location[1]
                ))

    # Upgrades
    for event in replay.tracker_events:
        if event.name == "UpgradeCompleteEvent":
            cursor.execute("""
                INSERT INTO upgrades (player_id, name, completed_at)
                VALUES (?, ?, ?)
            """, (
                event.player.pid,
                event.upgrade_type_name,
                event.second
            ))

    # Command Events
    for event in replay.events:
        if event.name in ('TargetPointCommandEvent', 'TargetUnitCommandEvent'):
            cursor.execute("""
                INSERT INTO command_events (player_id, timeline_id, x, y, ability_name, target_unit_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                event.player.pid,
                tick_map.get(event.frame, 0),
                event.location[0],
                event.location[1],
                event.ability_name,
                getattr(event, 'target_unit_id', None)
            ))

    # Player APM
    for player in replay.players:
        epm_data = calculate_epm(replay, player.pid)
        for second, apm in player.apm.items():
            timeline_id = second_to_timeline_id.get(second)
            if timeline_id:
                epm = epm_data.get(second, 0)
                cursor.execute("""
                    INSERT INTO player_apm (player_id, timeline_id, apm, epm)
                    VALUES (?, ?, ?, ?)
                """, (player.pid, timeline_id, round(apm), epm))

    conn.commit()
    conn.close()
    print("Replay parsed and data saved to SQLite.")

# This script is intended to be used as a module.