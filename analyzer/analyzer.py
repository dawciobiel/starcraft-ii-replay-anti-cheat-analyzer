# analyzer/analyzer.py

import sqlite3
import math

SUSPICIOUS_TIME_LIMIT = 30  # sekundy

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def analyze_maphack(db_path, output_dir):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Pobierz wszystkich graczy
    cursor.execute("SELECT player_id FROM players")
    players = [row[0] for row in cursor.fetchall()]

    # Pobierz wszystkie struktury (bazy) z timeline < 30s
    cursor.execute("""
        SELECT s.player_id, s.x, s.y, t.second
        FROM structures s
        JOIN timeline t ON s.timeline_id = t.timeline_id
        WHERE t.second <= ? AND s.name IN ('CommandCenter', 'OrbitalCommand', 'PlanetaryFortress', 'Nexus', 'Hatchery', 'Lair', 'Hive')
    """, (SUSPICIOUS_TIME_LIMIT,))
    bases = cursor.fetchall()

    # Pobierz wszystkie zdarzenia kamery z timeline < 30s
    cursor.execute("""
        SELECT c.player_id, c.x, c.y, t.second
        FROM camera_events c
        JOIN timeline t ON c.timeline_id = t.timeline_id
        WHERE t.second <= ?
    """, (SUSPICIOUS_TIME_LIMIT,))
    cameras = cursor.fetchall()

    # Sprawdź, czy któryś gracz patrzył na bazę przeciwnika
    for cam_player, cam_x, cam_y, cam_sec in cameras:
        for base_player, base_x, base_y, base_sec in bases:
            if cam_player != base_player:
                dist = distance(cam_x, cam_y, base_x, base_y)
                if dist < 10:  # próg podejrzanej odległości
                    cursor.execute("""
                        INSERT INTO alerts (player_id, tick, type, description)
                        VALUES (?, ?, ?, ?)
                    """, (
                        cam_player,
                        int(cam_sec * 16),  # tick = sekundy * 16 (SC2 tickrate)
                        "maphack",
                        f"Kamera gracza #{cam_player} była {dist:.1f} jednostek od bazy gracza #{base_player} w {cam_sec:.1f}s"
                    ))

    conn.commit()
    conn.close()
    print("Analiza zakończona. Alerty zapisane w bazie.")

# This script is intended to be used as a module.
