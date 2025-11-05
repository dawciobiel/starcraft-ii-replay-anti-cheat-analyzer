# analyzer/rules/unnatural_camera_movement/unnatural_camera_movement_v1.0.py

import math

SUSPICIOUS_TIME_LIMIT = 30  # seconds

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def analyze(db_cursor):
    """
    Analyzes the replay data for unnatural camera movements.

    Args:
        db_cursor: A cursor to the parsed replay database.

    Yields:
        A dictionary representing an alert if suspicious behavior is detected.
    """
    # Get all main structures (bases) within the suspicious time limit
    db_cursor.execute("""
        SELECT s.player_id, s.x, s.y, t.second
        FROM structures s
        JOIN timeline t ON s.timeline_id = t.timeline_id
        WHERE t.second <= ? AND s.name IN ('CommandCenter', 'OrbitalCommand', 'PlanetaryFortress', 'Nexus', 'Hatchery', 'Lair', 'Hive')
    """, (SUSPICIOUS_TIME_LIMIT,))
    bases = db_cursor.fetchall()

    # Get all camera events within the suspicious time limit
    db_cursor.execute("""
        SELECT c.player_id, c.x, c.y, t.second
        FROM camera_events c
        JOIN timeline t ON c.timeline_id = t.timeline_id
        WHERE t.second <= ?
    """, (SUSPICIOUS_TIME_LIMIT,))
    cameras = db_cursor.fetchall()

    # Check if any player looked at an opponent's base
    for cam_player, cam_x, cam_y, cam_sec in cameras:
        for base_player, base_x, base_y, base_sec in bases:
            if cam_player != base_player:
                dist = distance(cam_x, cam_y, base_x, base_y)
                if dist < 10:  # threshold for suspicious distance
                    yield {
                        'player_id': cam_player,
                        'tick': int(cam_sec * 16),  # tick = seconds * 16 (SC2 tickrate)
                        'type': 'UnnaturalCameraMovement',
                        'description': f"Player #{cam_player} camera was {dist:.1f} units from opponent's base #{base_player} at {cam_sec:.1f}s"
                    }