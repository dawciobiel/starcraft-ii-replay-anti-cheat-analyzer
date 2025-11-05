# Selection of Unseen Units

This document describes the procedure for detecting the selection of units or structures that are not visible to the player, which is a strong indicator of maphack usage.

## Description

If a player selects an enemy unit or structure in an area of the map where they do not have vision, it is a 100% certain indicator of a maphack.

## Detection Logic

The detection logic for this rule involves the following steps:

1.  **Monitor selection events:** Track the player's unit and structure selections (`command_events` table with `TargetUnitCommandEvent`).
2.  **Determine player vision:** For each selection event, determine the player's vision at that point in time. This requires a more complex analysis of the game state, including the positions of the player's units and structures.
3.  **Check for visibility:** Check if the selected unit or structure was actually visible to the player at the time of selection.
4.  **Generate an alert:** If a player selects a unit or structure that is not in their vision, generate a high-priority alert for maphack usage.