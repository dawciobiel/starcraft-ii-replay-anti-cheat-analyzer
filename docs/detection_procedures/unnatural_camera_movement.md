# Unnatural Camera Movement

This document describes the procedure for detecting unnatural camera movements that may indicate the use of a maphack.

## Description

If a player in the initial phase of the match moves their screen point of view to a location on the map far from their starting base, and this location contains enemy units or buildings, it is highly probable that they are using a maphack.

## Detection Logic

The detection logic for this rule involves the following steps:

1.  **Define the "initial phase":** This is typically the first few minutes of the game (e.g., the first 3 minutes).
2.  **Monitor camera events:** Track the player's camera movements (`camera_events` table).
3.  **Identify suspicious movements:** Look for camera movements to locations that are far from the player's known buildings and units.
4.  **Check for enemy presence:** At the time of the suspicious camera movement, check if there are any enemy units or structures at the camera's destination.
5.  **Generate an alert:** If all of the above conditions are met, generate an alert for potential maphack usage.