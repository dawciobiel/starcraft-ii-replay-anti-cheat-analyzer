# visualizer/visualizer.py

import sqlite3
import matplotlib.pyplot as plt
import os
import re
import configparser

def plot_camera_movements(player_id, db_path, output_dir, default_sanitized_name, show_own_bases=True, show_allied_bases=True, show_enemy_bases=True):
    # Read colors from config
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    color_camera = config.get('VisualizerColors', 'camera_positions', fallback='blue')
    color_own = config.get('VisualizerColors', 'own_bases', fallback='yellow')
    color_allied = config.get('VisualizerColors', 'allied_bases', fallback='green')
    color_enemy = config.get('VisualizerColors', 'enemy_bases', fallback='red')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get player's name and team
    cursor.execute("SELECT name, team FROM players WHERE player_id = ?", (player_id,))
    player_info = cursor.fetchone()
    if not player_info:
        print(f"Player with ID {player_id} not found.")
        conn.close()
        return
    player_name, player_team = player_info

    # Camera positions
    cursor.execute("""
        SELECT c.x, c.y, t.second
        FROM camera_events c
        JOIN timeline t ON c.timeline_id = t.timeline_id
        WHERE c.player_id = ?
    """, (player_id,))
    camera_data = cursor.fetchall()

    # Own bases
    own_bases = []
    if show_own_bases:
        cursor.execute("""
            SELECT s.x, s.y
            FROM structures s
            WHERE s.player_id = ?
        """, (player_id,))
        own_bases = cursor.fetchall()

    # Allied bases
    allied_bases = []
    if show_allied_bases:
        cursor.execute("""
            SELECT s.x, s.y
            FROM structures s
            JOIN players p ON s.player_id = p.player_id
            WHERE p.team = ? AND s.player_id != ?
        """, (player_team, player_id))
        allied_bases = cursor.fetchall()

    # Enemy bases
    enemy_bases = []
    if show_enemy_bases:
        cursor.execute("""
            SELECT s.x, s.y
            FROM structures s
            JOIN players p ON s.player_id = p.player_id
            WHERE p.team != ?
        """, (player_team,))
        enemy_bases = cursor.fetchall()

    conn.close()

    # Plot
    plt.figure(figsize=(8, 8))
    x_vals = [x for x, y, sec in camera_data]
    y_vals = [y for x, y, sec in camera_data]
    plt.scatter(x_vals, y_vals, c=color_camera, label='Camera Positions', alpha=0.6)

    # Own bases
    if own_bases:
        base_x = [x for x, y in own_bases]
        base_y = [y for x, y in own_bases]
        plt.scatter(base_x, base_y, c=color_own, marker='s', label='Own Bases')

    # Allied bases
    if allied_bases:
        base_x = [x for x, y in allied_bases]
        base_y = [y for x, y in allied_bases]
        plt.scatter(base_x, base_y, c=color_allied, marker='s', label='Allied Bases')

    # Enemy bases
    if enemy_bases:
        base_x = [x for x, y in enemy_bases]
        base_y = [y for x, y in enemy_bases]
        plt.scatter(base_x, base_y, c=color_enemy, marker='X', label='Enemy Bases')

    plt.title(f"Camera Movements for {player_name}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # Sanitize player name for use in filename
    sanitized_name = player_name.encode('ascii', 'ignore').decode('ascii')
    sanitized_name = re.sub(r'[^\w_]+', '_', sanitized_name)
    sanitized_name = re.sub(r'__+', '_', sanitized_name)
    sanitized_name = sanitized_name.strip('_')
    if not sanitized_name:
        sanitized_name = default_sanitized_name

    # Construct output filename
    file_name = f"player_{player_id}_{sanitized_name}_camera.png"
    output_file = os.path.join(output_dir, file_name)
    plt.savefig(output_file)
    print(f"📊 Wykres ruchów kamery zapisany do: {output_file}")

# This script is intended to be used as a module.
