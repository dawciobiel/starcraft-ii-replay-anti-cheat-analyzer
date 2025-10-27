# cli.py

import argparse
import os
from parser.parser import parse_replay
from analyzer.analyzer import analyze_maphack
from visualizer.visualizer import plot_camera_movements

def main():
    parser = argparse.ArgumentParser(
        description="StarCraft II Replay Anti-Cheat Analyzer CLI"
    )
    parser.add_argument("replay", help="Ścieżka do pliku .SC2Replay")
    parser.add_argument("--analyze", action="store_true", help="Uruchom analizę maphacka")
    parser.add_argument("--visualize", type=int, metavar="PLAYER_ID", help="Wizualizuj ruchy kamery danego gracza")

    args = parser.parse_args()

    if not os.path.exists(args.replay):
        print("❌ Plik replay nie istnieje.")
        return

    print("📥 Parsowanie replaya...")
    parse_replay(args.replay)

    if args.analyze:
        print("🔍 Uruchamiam analizę maphacka...")
        analyze_maphack()

    if args.visualize is not None:
        print(f"📊 Wizualizacja ruchów kamery gracza #{args.visualize}...")
        plot_camera_movements(player_id=args.visualize)

if __name__ == "__main__":
    main()
