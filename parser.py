# parser/parser.py

import sc2reader
import sqlite3
import os

DB_PATH = "replay_data.db"

def init_db():
    with open("schema.sql", "r") as f:
        schema = f.read()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema)
    conn.commit()
    return conn

def parse_replay(replay_path):
    replay = sc2reader.load_replay(replay_path, load_level=4)
    conn = init_db()
    cursor = conn.cursor()

    # Players
    for player in replay.players:
        cursor.execute("""
            INSERT INTO players (player_id, name, race, team, color)
            VALUES (?, ?, ?, ?, ?)
        """, (player.pid, player.name, player.play_race, player.team, player.color.hex))

    # Timeline
    tick_map = {}
    for i, event in enumerate(replay.tracker_events):
        tick = event.frame
        second = event.second
        tick_map[tick] = i + 1
        cursor.execute("INSERT INTO timeline (timeline_id, tick, second) VALUES (?, ?, ?)", (i + 1, tick, second))

    # Structures
    for event in replay.tracker_events:
        if event.name == "UnitInitEvent" and event.unit.is_building:
            cursor.execute("""
                INSERT INTO structures (player_id, name, x, y, elevation_level, is_flying, timeline_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                event.unit.owner.pid,
                event.unit.name,
                event.unit.x,
                event.unit.y,
                None,  # elevation_level (optional)
                False,  # is_flying
                tick_map.get(event.frame)
            ))

    # Units
    for event in replay.tracker_events:
        if event.name == "UnitBornEvent" and not event.unit.is_building:
            cursor.execute("""
                INSERT INTO units (player_id, name, x, y, hp, shield, energy, timeline_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.unit.owner.pid,
                event.unit.name,
                event.unit.x,
                event.unit.y,
                event.unit.health,
                getattr(event.unit, "shield", 0),
                getattr(event.unit, "energy", 0),
                tick_map.get(event.frame)
            ))

    # Camera Events
    for event in replay.tracker_events:
        if event.name == "CameraEvent":
            cursor.execute("""
                INSERT INTO camera_events (player_id, x, y, timeline_id)
                VALUES (?, ?, ?, ?)
            """, (
                event.player.pid,
                event.x,
                event.y,
                tick_map.get(event.frame)
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

    conn.commit()
    conn.close()
    print("Replay parsed and data saved to SQLite.")

if __name__ == "__main__":
    replay_file = "replays/game.SC2Replay"
    if os.path.exists(replay_file):
        parse_replay(replay_file)
    else:
        print("Replay file not found.")
