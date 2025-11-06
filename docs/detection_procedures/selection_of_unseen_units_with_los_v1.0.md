# Selection of Unseen Units with Line of Sight (v1.0)

## Description
This rule detects suspicious player behavior where units are selected that should not be visible based on their line of sight (LoS) and terrain elevation.

Unlike the basic `selection_of_unseen_units` rule, this advanced version takes into account the 'z' (elevation) coordinate of units and structures. It uses a simplified Line of Sight model to determine if there are significant elevation differences between a player's unit and an enemy unit that would block vision.

## Detection Logic
1.  **Data Retrieval:** For each `SelectionEvent`, the rule retrieves the `player_id`, `timeline_id`, and the `selected_unit_ids`.
2.  **Unit Position and Elevation:** It fetches the `x`, `y`, and `z` (elevation) coordinates for both the selected enemy unit(s) and all of the player's own units/structures at the given `timeline_id`.
3.  **Vision Range Check:** For each selected enemy unit, the rule iterates through all of the player's units/structures to determine if any of them could provide vision.
4.  **Line of Sight (LoS) Check:** In addition to the standard vision range, a `has_line_of_sight` function is used. This function checks the absolute difference in 'z' coordinates between the player's unit and the enemy unit. If the elevation difference exceeds a predefined `ELEVATION_THRESHOLD` (currently 2 units), it is assumed that line of sight is blocked, regardless of horizontal distance.
5.  **Alert Generation:** If a selected enemy unit is found to be outside the vision range of all player units/structures, OR if it is within range but the line of sight is blocked by terrain elevation, an alert of type `SelectionOfUnseenUnitWithLoS` is generated.

## Configuration
-   `ELEVATION_THRESHOLD`: A constant defined within the rule (`ELEVATION_THRESHOLD = 2`). This value determines the maximum allowed elevation difference between two units for them to maintain line of sight. This can be adjusted to fine-tune the sensitivity of the rule.
-   `selection_of_unseen_units_v1.0.json`: This JSON file, located in the same directory as the rule, contains vision ranges for various units and buildings. This data is used to determine the horizontal vision range of player units.

## Future Improvements
-   **Advanced LoS Model:** Implement a more sophisticated Line of Sight algorithm that considers terrain geometry (e.g., cliffs, ramps) and map features (e.g., destructible rocks, foliage) that might block vision.
-   **Dynamic Vision Changes:** Account for temporary vision-granting abilities (e.g., Scanner Sweep, Raven's Point Defense Drone) or vision-blocking effects.
-   **Performance Optimization:** For large replays, optimize database queries and LoS calculations to reduce analysis time.