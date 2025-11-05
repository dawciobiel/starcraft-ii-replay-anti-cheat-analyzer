# analyzer/rules/camera_movement_to_unseen_enemy/camera_movement_to_unseen_enemy_v1.0.py

import math
import os
import json

# Import vision data loading from the other plugin
from analyzer.rules.selection_of_unseen_units.selection_of_unseen_units_v1_0 import load_vision_ranges, get_vision_range

# Define a reasonable radius for camera movement inspection
# If a camera moves to a location, we check a small radius around it for enemy units
CAMERA_INSPECTION_RADIUS = 5

def distance(x1, y1, x2, y2):
    if x1 is None or y1 is None or x2 is None or y2 is None:
        return float('inf')
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def analyze(db_cursor):
    """
    Analyzes for camera movements to unseen enemy units or structures.
    """
    vision_data = load_vision_ranges()

    # Get all camera events
    db_cursor.execute("""
        SELECT player_id, timeline_id, x, y
        FROM camera_events
    """)
    camera_events = db_cursor.fetchall()

    for player_id, timeline_id, cam_x, cam_y in camera_events:
        # Get all enemy units/structures at that timeline
        db_cursor.execute("""
            SELECT u.unit_id, u.name, u.x, u.y FROM units u WHERE u.timeline_id = ? AND u.player_id NOT IN (SELECT player_id FROM players WHERE team = (SELECT team FROM players WHERE player_id = ?))
            UNION ALL
            SELECT s.structure_id, s.name, s.x, s.y FROM structures s WHERE s.timeline_id = ? AND s.player_id NOT IN (SELECT player_id FROM players WHERE team = (SELECT team FROM players WHERE player_id = ?))
        """, (timeline_id, player_id, timeline_id, player_id))
        enemy_objects = db_cursor.fetchall()

        # Get all player and ally units/structures at that timeline
        db_cursor.execute("""
            SELECT u.name, u.x, u.y FROM units u WHERE u.timeline_id = ? AND u.player_id IN (SELECT player_id FROM players WHERE team = (SELECT team FROM players WHERE player_id = ?))
            UNION ALL
            SELECT s.name, s.x, s.y FROM structures s WHERE s.timeline_id = ? AND s.player_id IN (SELECT player_id FROM players WHERE team = (SELECT team FROM players WHERE player_id = ?))
        """, (timeline_id, player_id, timeline_id, player_id))
        player_ally_objects = db_cursor.fetchall()

        for enemy_id, enemy_name, enemy_x, enemy_y in enemy_objects:
            # Check if the camera is near an enemy object
            if distance(cam_x, cam_y, enemy_x, enemy_y) <= CAMERA_INSPECTION_RADIUS:
                is_visible = False
                for player_ally_name, player_ally_x, player_ally_y in player_ally_objects:
                    dist_to_enemy = distance(enemy_x, enemy_y, player_ally_x, player_ally_y)
                    player_ally_vision_range = get_vision_range(player_ally_name, vision_data)

                    # If any player/ally unit can see the enemy object
                    if dist_to_enemy <= player_ally_vision_range:
                        is_visible = True
                        break
                
                if not is_visible:
                    db_cursor.execute("SELECT tick FROM timeline WHERE timeline_id = ?", (timeline_id,))
                    tick = db_cursor.fetchone()[0]
                    yield {
                        'player_id': player_id,
                        'tick': tick,
                        'type': 'CameraMovementToUnseenEnemy',
                        'description': f"Player #{player_id} moved camera to unseen enemy {enemy_name} (ID: {enemy_id}) at ({enemy_x}, {enemy_y})."
                    }
