# Logged Data from Replays

This document outlines the data extracted from StarCraft II replays and stored in the database. This list will be updated as new data points are added to the parser.

## Tables and Their Contents

### `players`
Stores information about each player in the replay.
- `player_id`: Unique identifier for the player.
- `name`: Player's in-game name.
- `toon_id`: Player's Toon ID.
- `bnet_url`: Player's Battle.net profile URL.
- `race`: Player's chosen race (e.g., Terran, Zerg, Protoss).
- `team`: Player's team number.
- `color`: Player's in-game color.
- `mmr`: MMR of the player in this game mode.
- `enemy_workers_killed`: Enemy workers killed by this player.

### `timeline`
Maps game ticks and seconds to a unique timeline ID.
- `timeline_id`: Unique identifier for a point in the game timeline.
- `tick`: Game tick (frame).
- `second`: Game second.

### `structures`
Records details about buildings constructed or initialized during the game.
- `structure_id`: Unique identifier for the structure.
- `player_id`: Foreign key to the `players` table.
- `name`: Name of the structure (e.g., CommandCenter, Nexus).
- `x`: X-coordinate of the structure's location.
- `y`: Y-coordinate of the structure's location.
- `elevation_level`: Elevation level of the structure (optional).
- `is_flying`: Boolean indicating if the structure is flying.
- `timeline_id`: Foreign key to the `timeline` table, indicating when the structure was created/initialized.

### `units`
Records details about units born during the game.
- `unit_id`: Unique identifier for the unit.
- `player_id`: Foreign key to the `players` table.
- `name`: Name of the unit (e.g., Marine, Zealot).
- `x`: X-coordinate of the unit's location.
- `y`: Y-coordinate of the unit's location.
- `hp`: Health points of the unit.
- `shield`: Shield points of the unit.
- `energy`: Energy points of the unit.
- `timeline_id`: Foreign key to the `timeline` table, indicating when the unit was born.

### `camera_events`
Logs camera movements for each player.
- `camera_id`: Unique identifier for the camera event.
- `player_id`: Foreign key to the `players` table.
- `x`: X-coordinate of the camera's position.
- `y`: Y-coordinate of the camera's position.
- `timeline_id`: Foreign key to the `timeline` table, indicating when the camera event occurred.

### `upgrades`
Tracks completed upgrades for each player.
- `upgrade_id`: Unique identifier for the upgrade.
- `player_id`: Foreign key to the `players` table.
- `name`: Name of the completed upgrade.
- `completed_at`: Game second when the upgrade was completed.

### `alerts`
Stores alerts generated during maphack analysis.
- `alert_id`: Unique identifier for the alert.
- `player_id`: Foreign key to the `players` table.
- `tick`: Game tick when the alert occurred.
- `type`: Type of alert (e.g., "Maphack Detected").
- `description`: Detailed description of the alert.

### `command_events`
Records player command events.
- `command_id`: Unique identifier for the command event.
- `player_id`: Foreign key to the `players` table.
- `timeline_id`: Foreign key to the `timeline` table, indicating when the command occurred.
- `x`: X-coordinate of the command's target location.
- `y`: Y-coordinate of the command's target location.
- `ability_name`: Name of the ability used in the command.
- `target_unit_id`: ID of the target unit for the command (if applicable).

### `player_apm`
Stores Actions Per Minute (APM) and Effective Actions Per Minute (EPM) for each player over time.
- `apm_id`: Unique identifier for the APM/EPM record.
- `player_id`: Foreign key to the `players` table.
- `timeline_id`: Foreign key to the `timeline` table, indicating the game second for the APM/EPM value.
- `apm`: Actions Per Minute value.
- `epm`: Effective Actions Per Minute value.