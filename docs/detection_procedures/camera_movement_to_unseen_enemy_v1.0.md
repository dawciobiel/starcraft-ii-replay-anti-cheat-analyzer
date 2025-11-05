# Camera Movement to Unseen Enemy

This document describes the procedure for detecting camera movements to enemy units or structures in areas where the player lacks vision, which is a strong indicator of maphack usage.

## Description

If a player moves their camera view to an enemy unit or building on the map, and they do not have legitimate vision in that area (i.e., no friendly units or structures are present to provide vision), it is a strong indicator of maphack usage.

## Detection Logic

The detection logic for this rule involves the following steps:

1.  **Monitor camera events:** Track the player's camera movements (`camera_events` table).
2.  **Determine player vision:** For each camera movement, determine the player's vision at that point in time. This requires analyzing the positions of the player's units and structures.
3.  **Check for enemy presence:** At the camera's destination, check if there are any enemy units or structures present.
4.  **Verify lack of vision:** Confirm that the player does not have legitimate vision in the area where the camera moved to the enemy unit/structure.
5.  **Generate an alert:** If all of the above conditions are met, generate a high-priority alert for maphack usage.
