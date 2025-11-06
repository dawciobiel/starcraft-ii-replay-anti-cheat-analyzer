from analyzer.analyzer import BaseRule
import math
import os
import json

# Define a reasonable radius for camera movement inspection
# If a camera moves to a location, we check a small radius around it for enemy units
CAMERA_INSPECTION_RADIUS = 5

def distance(x1, y1, x2, y2):
    if x1 is None or y1 is None or x2 is None or y2 is None:
        return float('inf')
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class CameraMovementToUnseenEnemyV10(BaseRule):
    def __init__(self, db_path):
        super().__init__(db_path)
        self.vision_data = self._load_vision_ranges()

    def _load_vision_ranges(self):
        """Loads vision ranges from the JSON config file."""
        # This rule uses the same vision data config as selection_of_unseen_units
        CONFIG_FILE_NAME = "selection_of_unseen_units_v1.0.json"
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "selection_of_unseen_units", CONFIG_FILE_NAME)
        with open(config_path, 'r') as f:
            return json.load(f)

    def _get_vision_range(self, unit_name):
        """Gets the vision range for a given unit or building name."""
        if unit_name in self.vision_data['units']:
            return self.vision_data['units'][unit_name]
        # Assuming it's a building if not found in units
        return self.vision_data['buildings']['default']

    def run(self):
        """
        Analyzes for camera movements to unseen enemy units or structures.
        """
        self.connect_db()

        # Get all camera events
        self.cursor.execute("""
            SELECT player_id, timeline_id, x, y
            FROM camera_events
        """
        )
        camera_events = self.cursor.fetchall()

        for player_id, timeline_id, cam_x, cam_y in camera_events:
            # Get all enemy units/structures at that timeline
            self.cursor.execute("""
                SELECT u.unit_id, u.name, u.x, u.y FROM units u WHERE u.timeline_id = ? AND u.player_id NOT IN (SELECT player_id FROM players WHERE team = (SELECT team FROM players WHERE player_id = ?))
                UNION ALL
                SELECT s.structure_id, s.name, s.x, s.y FROM structures s WHERE s.timeline_id = ? AND s.player_id NOT IN (SELECT player_id FROM players WHERE team = (SELECT team FROM players WHERE player_id = ?))
            """, (timeline_id, player_id, timeline_id, player_id))
            enemy_objects = self.cursor.fetchall()

            # Get all player and ally units/structures at that timeline
            self.cursor.execute("""
                SELECT u.name, u.x, u.y FROM units u WHERE u.timeline_id = ? AND u.player_id IN (SELECT player_id FROM players WHERE team = (SELECT team FROM players WHERE player_id = ?))
                UNION ALL
                SELECT s.name, s.x, s.y FROM structures s WHERE s.timeline_id = ? AND s.player_id IN (SELECT player_id FROM players WHERE team = (SELECT team FROM players WHERE player_id = ?))
            """, (timeline_id, player_id, timeline_id, player_id))
            player_ally_objects = self.cursor.fetchall()

            for enemy_id, enemy_name, enemy_x, enemy_y in enemy_objects:
                # Check if the camera is near an enemy object
                if distance(cam_x, cam_y, enemy_x, enemy_y) <= CAMERA_INSPECTION_RADIUS:
                    is_visible = False
                    for player_ally_name, player_ally_x, player_ally_y in player_ally_objects:
                        dist_to_enemy = distance(enemy_x, enemy_y, player_ally_x, player_ally_y)
                        player_ally_vision_range = self._get_vision_range(player_ally_name)

                        # If any player/ally unit can see the enemy object
                        if dist_to_enemy <= player_ally_vision_range:
                            is_visible = True
                            break
                    
                    if not is_visible:
                        self.cursor.execute("SELECT tick FROM timeline WHERE timeline_id = ?", (timeline_id,))
                        tick = self.cursor.fetchone()[0]
                        self._insert_alert(
                            player_id=player_id,
                            tick=tick,
                            type='CameraMovementToUnseenEnemy',
                            description=f"Player #{player_id} moved camera to unseen enemy {enemy_name} (ID: {enemy_id}) at ({enemy_x}, {enemy_y})."
                        )
        self.close_db()
