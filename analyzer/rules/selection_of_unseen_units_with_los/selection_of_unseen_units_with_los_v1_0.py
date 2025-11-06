from analyzer.analyzer import BaseRule
import math
import json
import os

ELEVATION_THRESHOLD = 2

def distance(x1, y1, x2, y2):
    if x1 is None or y1 is None or x2 is None or y2 is None:
        return float('inf')
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def has_line_of_sight(z1, z2):
    if z1 is None or z2 is None:
        return True # Assume line of sight if elevation data is missing
    return abs(z1 - z2) <= ELEVATION_THRESHOLD

class SelectionOfUnseenUnitsWithLoSV10(BaseRule):
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
        Analyzes for selection of unseen units, taking line of sight into account.
        """
        self.connect_db()

        # Get all selection events of enemy units
        self.cursor.execute("""
            SELECT player_id, timeline_id, selected_unit_ids
            FROM selection_events
        """
        )
        selection_events = self.cursor.fetchall()

        for player_id, timeline_id, selected_unit_ids_str in selection_events:
            if not selected_unit_ids_str:
                continue

            selected_unit_ids = [int(uid) for uid in selected_unit_ids_str.split(',')]

            # Get all player units/structures at that timeline
            self.cursor.execute("""
                SELECT name, x, y, z FROM units WHERE timeline_id = ? AND player_id = ?
                UNION ALL
                SELECT name, x, y, z FROM structures WHERE timeline_id = ? AND player_id = ?
            """, (timeline_id, player_id, timeline_id, player_id))
            player_units = self.cursor.fetchall()

            for selected_unit_id in selected_unit_ids:
                # Get the selected enemy unit's details
                self.cursor.execute("SELECT name, x, y, z FROM units WHERE unit_id = ?", (selected_unit_id,))
                enemy_unit = self.cursor.fetchone()
                if not enemy_unit:
                    self.cursor.execute("SELECT name, x, y, z FROM structures WHERE structure_id = ?", (selected_unit_id,))
                    enemy_unit = self.cursor.fetchone()

                if not enemy_unit:
                    continue

                enemy_name, enemy_x, enemy_y, enemy_z = enemy_unit

                is_visible = False
                for player_unit_name, player_unit_x, player_unit_y, player_unit_z in player_units:
                    dist = distance(enemy_x, enemy_y, player_unit_x, player_unit_y)
                    player_vision_range = self._get_vision_range(player_unit_name)

                    if dist <= player_vision_range and has_line_of_sight(enemy_z, player_unit_z):
                        is_visible = True
                        break
                
                if not is_visible:
                    self.cursor.execute("SELECT tick FROM timeline WHERE timeline_id = ?", (timeline_id,))
                    tick = self.cursor.fetchone()[0]
                    self._insert_alert(
                        player_id=player_id,
                        tick=tick,
                        type='SelectionOfUnseenUnitWithLoS',
                        description=f"Player #{player_id} selected unit {enemy_name} (ID: {selected_unit_id}) which was not in their line of sight."
                    )
        self.close_db()
