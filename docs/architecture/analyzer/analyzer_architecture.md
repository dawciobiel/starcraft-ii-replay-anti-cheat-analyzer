# Application Architecture

This document outlines the architecture of the StarCraft II Replay Anti-Cheat Analyzer. The primary goal is to create a modular, extensible, and maintainable system for detecting cheating in replay files.

## Core Components

The system is composed of three main components:

1.  **Parser (`parser.py`):** A module responsible for reading a `.SC2Replay` file and transforming its data into a structured, queryable format.
2.  **Analyzer (`analyzer.py`):** The central orchestrator. It discovers, configures, and runs all available analysis plugins.
3.  **Plugins/Rules (`analyzer/rules/`):** A directory containing individual, independent Python modules. Each module defines one or more cheat detection rules as classes inheriting from `BaseRule` (e.g., checking for unnatural camera movement).

## Data Flow and Storage

To ensure decoupling, versionability, and clarity, the application uses a specific file and directory structure for storing analysis artifacts.

### 1. Analysis Directory Structure

For each replay file that is analyzed (e.g., `my-replay.SC2Replay`), a unique, timestamped directory is created to store all results from that specific analysis run.

```
replays-analysis/
└── my-replay/
    └── 2025-11-05_23-55-00/
        ├── ... (analysis artifacts)
```

### 2. Parser Output

The **Parser** takes the raw replay file as input and produces a structured SQLite database containing the parsed game data (players, units, events, etc.). This database is stored within the analysis directory.

- **Output:** `.../YYYY-MM-DD_HH-MM-SS/parser-v1.0.db`

### 3. Plugin Data Storage

If a **Plugin** requires its own persistent data storage for complex, intermediate calculations, it is responsible for creating its own SQLite database within the same analysis directory. The plugin must manage its own database schema.

- **Example Output:** `.../YYYY-MM-DD_HH-MM-SS/unnatural_camera_movement-v1.0.db`

### 4. Final Output and Alerts

Plugins **now directly insert their findings into the main analysis database.** When a plugin detects a suspicious action, it inserts an entry into the `alerts` table within the `parser-v1.0.db`.

After all plugins have completed their analysis, the `Analyzer` retrieves all alerts from the `alerts` table and serializes this list into a single, comprehensive JSON file in the analysis directory.

- **Final Output:** `.../YYYY-MM-DD_HH-MM-SS/alerts.json`

## Execution Model

1.  **Plugin Discovery:** The `Analyzer` automatically discovers all available rules by scanning the `analyzer/rules/` directory. It identifies classes inheriting from `BaseRule`.
2.  **Parallel Execution:** To ensure efficiency, the `Analyzer` runs the analysis for each discovered plugin in parallel (e.g., using a `ThreadPoolExecutor`).
3.  **Plugin Interface:** All plugins must adhere to a common interface by inheriting from the `BaseRule` abstract class. This ensures that the `Analyzer` can interact with each plugin in a standardized way by instantiating the rule class and calling its `run()` method. The `BaseRule` class provides methods for database connection and alert insertion.
