# visualizer/visualizer.py

import sqlite3
import matplotlib.pyplot as plt
import os
import re

def plot_camera_movements(player_id, db_path, output_dir, default_sanitized_name, show_enemy_bases=True):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Pobierz nick gracza
    cursor.execute("SELECT name FROM players WHERE player_id = ?", (player_id,))
    player_name = cursor.fetchone()[0]

    # Pozycje kamery
    cursor.execute("""
        SELECT c.x, c.y, t.second
        FROM camera_events c
        JOIN timeline t ON c.timeline_id = t.timeline_id
        WHERE c.player_id = ?
    """, (player_id,))
    camera_data = cursor.fetchall()

    # Pozycje baz przeciwników
    enemy_bases = []
    if show_enemy_bases:
        cursor.execute("""
            SELECT s.x, s.y
            FROM structures s
            WHERE s.player_id != ?
        """, (player_id,))
        enemy_bases = cursor.fetchall()

    conn.close()

    # Wykres
    plt.figure(figsize=(8, 8))
    x_vals = [x for x, y, sec in camera_data]
    y_vals = [y for x, y, sec in camera_data]
    plt.scatter(x_vals, y_vals, c='blue', label='Camera Positions', alpha=0.6)

    # Bazy przeciwników
    if enemy_bases:
        base_x = [x for x, y in enemy_bases]
        base_y = [y for x, y in enemy_bases]
        plt.scatter(base_x, base_y, c='red', marker='X', label='Enemy Bases')

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
