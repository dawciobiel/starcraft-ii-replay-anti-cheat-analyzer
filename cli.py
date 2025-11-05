# cli.py

import argparse
import os
import datetime
import configparser
import sqlite3
from parser.parser import parse_replay
from analyzer.analyzer import analyze_replay
from visualizer.visualizer import plot_camera_movements

def main():
    parser = argparse.ArgumentParser(
        description="StarCraft II Replay Anti-Cheat Analyzer CLI"
    )
    parser.add_argument("replay", help="Ścieżka do pliku .SC2Replay")
    parser.add_argument("--analyze", action="store_true", help="Uruchom analizę maphacka")
    parser.add_argument("--visualize", action="store_true", help="Wizualizuj ruchy kamery dla wszystkich graczy")

    args = parser.parse_args()

    if not os.path.exists(args.replay):
        print("❌ Plik replay nie istnieje.")
        return

    # Base analysis directory
    base_analysis_dir = "replays-analysis"
    os.makedirs(base_analysis_dir, exist_ok=True)

    # Extract replay name without extension
    replay_base_name = os.path.splitext(os.path.basename(args.replay))[0]

    # Read configuration
    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini')
    timestamp_format = config.get('Analyzer', 'TimestampFormat', fallback='%Y-%m-%d_%H-%M-%S')
    default_sanitized_name = config.get('Analyzer', 'DefaultSanitizedName', fallback='unicode_characters_name')

    # Generate timestamp for the analysis run
    timestamp = datetime.datetime.now().strftime(timestamp_format)

    # Create the unique analysis directory: replays-analysis/REPLAY_NAME/TIMESTAMP/
    current_analysis_dir = os.path.join(base_analysis_dir, replay_base_name, timestamp)
    os.makedirs(current_analysis_dir, exist_ok=True)

    # Construct the parser's database path
    parser_db_name = f"{replay_base_name}.parser-v1.0.db" # Assuming v1.0 for now
    db_path = os.path.join(current_analysis_dir, parser_db_name)

    print(f"📥 Parsowanie replaya i zapis do: {db_path}")
    parse_replay(args.replay, db_path)

    if args.analyze:
        print("🔍 Uruchamiam analizę...")
        analyze_replay(db_path, current_analysis_dir)

    if args.visualize:
        print("📊 Generowanie wizualizacji ruchów kamery dla wszystkich graczy...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT player_id FROM players")
        player_ids = [row[0] for row in cursor.fetchall()]
        conn.close()

        for player_id in player_ids:
            print(f"  -> Generowanie wykresu dla gracza #{player_id}...")
            plot_camera_movements(player_id=player_id, db_path=db_path, output_dir=current_analysis_dir, default_sanitized_name=default_sanitized_name)

if __name__ == "__main__":
    main()
