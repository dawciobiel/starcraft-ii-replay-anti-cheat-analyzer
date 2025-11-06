from analyzer.analyzer import BaseRule
import json
import os
import math

def distance(x1, y1, x2, y2):
    if x1 is None or y1 is None or x2 is None or y2 is None:
        return float('inf')
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class SelectionOfUnseenUnitsV10(BaseRule):
    def __init__(self, db_path):
        super().__init__(db_path)
        self.vision_data = self._load_vision_ranges()

    def _load_vision_ranges(self):
        """Loads vision ranges from the JSON config file."""
        CONFIG_FILE_NAME = "selection_of_unseen_units_v1.0.json"
        config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME)
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
        Analyzes for selection of unseen units.
        """
        self.connect_db()

        # Get all selection events of enemy units
        self.cursor.execute("""
            SELECT player_id, timeline_id, selected_unit_ids, camera_x, camera_y
            FROM selection_events
        """
        )
        selection_events = self.cursor.fetchall()

        for player_id, timeline_id, selected_unit_ids_str, cam_x, cam_y in selection_events:
            if not selected_unit_ids_str:
                continue

            selected_unit_ids = [int(uid) for uid in selected_unit_ids_str.split(',')]

            # Get all player and ally units/structures at that timeline
            self.cursor.execute("""
                SELECT u.name, u.x, u.y FROM units u WHERE u.timeline_id = ? AND u.player_id IN (SELECT player_id FROM players WHERE team = (SELECT team FROM players WHERE player_id = ?))
                UNION ALL
                SELECT s.name, s.x, s.y FROM structures s WHERE s.timeline_id = ? AND s.player_id IN (SELECT player_id FROM players WHERE team = (SELECT team FROM players WHERE player_id = ?))
            """, (timeline_id, player_id, timeline_id, player_id))
            player_units = self.cursor.fetchall()

            for selected_unit_id in selected_unit_ids:
                # Get the selected enemy unit's details
                self.cursor.execute("SELECT name, x, y FROM units WHERE unit_id = ?", (selected_unit_id,))
                enemy_unit = self.cursor.fetchone()
                if not enemy_unit:
                    self.cursor.execute("SELECT name, x, y FROM structures WHERE structure_id = ?", (selected_unit_id,))
                    enemy_unit = self.cursor.fetchone()

                if not enemy_unit:
                    continue

                enemy_name, enemy_x, enemy_y = enemy_unit
                enemy_vision_range = self._get_vision_range(enemy_name)

                is_visible = False
                for player_unit_name, player_unit_x, player_unit_y in player_units:
                    dist = distance(enemy_x, enemy_y, player_unit_x, player_unit_y)
                    player_vision_range = self._get_vision_range(player_unit_name)
                    
                    # Check if player unit is in enemy's vision (your logic)
                    if dist <= enemy_vision_range:
                        is_visible = True
                        break
                    # Also check if enemy unit is in player's vision (more direct check)
                    if dist <= player_vision_range:
                        is_visible = True
                        break
                
                if not is_visible:
                    self.cursor.execute("SELECT tick FROM timeline WHERE timeline_id = ?", (timeline_id,))
                    tick = self.cursor.fetchone()[0]
                    self._insert_alert(
                        player_id=player_id,
                        tick=tick,
                        type='SelectionOfUnseenUnit',
                        description=f"Player #{player_id} selected unit {enemy_name} (ID: {selected_unit_id}) which was not in their vision."
                    )
        self.close_db()
