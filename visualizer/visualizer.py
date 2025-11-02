# visualizer/visualizer.py

import sqlite3
import matplotlib.pyplot as plt

def plot_camera_movements(player_id, db_path, show_enemy_bases=True):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

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
    plt.scatter(x_vals, y_vals, c='blue', label='Pozycje kamery', alpha=0.6)

    # Bazy przeciwników
    if enemy_bases:
        base_x = [x for x, y in enemy_bases]
        base_y = [y for x, y in enemy_bases]
        plt.scatter(base_x, base_y, c='red', marker='X', label='Bazy przeciwników')

    plt.title(f"Ruchy kamery gracza #{player_id}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_camera_movements(player_id=1, db_path="replay_data.db")
