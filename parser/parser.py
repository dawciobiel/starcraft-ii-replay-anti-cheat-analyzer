import sc2reader
import sqlite3
import os

def init_db(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)
    with open("schema.sql", "r") as f:
        schema = f.read()
    conn = sqlite3.connect(db_path)
    conn.executescript(schema)
    conn.commit()
    return conn

def parse_replay(replay_path, db_path):
    replay = sc2reader.load_replay(replay_path, load_level=4)
    conn = init_db(db_path)
    cursor = conn.cursor()

    # Players
    for player in replay.players:
        cursor.execute("""
            INSERT INTO players (player_id, name, race, team, color)
            VALUES (?, ?, ?, ?, ?)
        """, (player.pid, player.name, player.play_race, player.team.number, player.color.hex))

    # Timeline
    tick_map = {}
    for i, event in enumerate(replay.tracker_events):
        tick = event.frame
        second = event.second
        tick_map[tick] = i + 1
        cursor.execute("INSERT INTO timeline (timeline_id, tick, second) VALUES (?, ?, ?)", (i + 1, tick, second))

    # Initial Structures
    initial_main_buildings = set()
    for unit in replay.objects.values():
        if unit.is_building and unit.owner and unit.name in ('CommandCenter', 'Nexus', 'Hatchery') and unit.owner.pid not in initial_main_buildings:
            initial_main_buildings.add(unit.owner.pid)
            cursor.execute("""
                INSERT INTO structures (player_id, name, x, y, elevation_level, is_flying, timeline_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                unit.owner.pid,
                unit.name,
                unit.location[0],
                unit.location[1],
                None,  # elevation_level (optional)
                False,  # is_flying
                1 # timeline_id for initial structures
            ))

    # Structures
    for event in replay.tracker_events:
        if event.name in ('UnitBornEvent', 'UnitInitEvent') and event.unit.is_building and event.unit.owner:
            cursor.execute("""
                INSERT INTO structures (player_id, name, x, y, elevation_level, is_flying, timeline_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                event.unit.owner.pid,
                event.unit.name,
                event.unit.location[0],
                                event.unit.location[1],
                                None,  # elevation_level (optional)
                                False,  # is_flying
                                                tick_map.get(event.frame, 0))
                                            )
    # Units
    for event in replay.tracker_events:
        if event.name == "UnitBornEvent" and not event.unit.is_building and event.unit.owner:
            cursor.execute("""
                INSERT INTO units (player_id, name, x, y, hp, shield, energy, timeline_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.unit.owner.pid,
                event.unit.name,
                event.unit.location[0],
                event.unit.location[1],
                getattr(event.unit, "health", None),
                getattr(event.unit, "shield", None),
                getattr(event.unit, "energy", None),
                tick_map.get(event.frame, 0)
            ))

    # Camera Events
    for event in replay.events:
        if event.name == "CameraEvent":
            cursor.execute("""
                INSERT INTO camera_events (player_id, x, y, timeline_id)
                VALUES (?, ?, ?, ?)
            """, (
                event.player.pid,
                event.x,
                event.y,
                tick_map.get(event.frame, 0))
            )

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

    conn.commit()
    conn.close()
    print("Replay parsed and data saved to SQLite.")

if __name__ == "__main__":
    replay_file = "replays/game.SC2Replay"
    if os.path.exists(replay_file):
        parse_replay(replay_file, "replay_data.db")
    else:
        print("Replay file not found.")