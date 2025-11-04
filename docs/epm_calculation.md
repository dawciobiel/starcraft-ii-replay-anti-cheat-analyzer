# EPM (Effective Actions Per Minute)

EPM values are calculated based on a custom logic implemented in the parser. The goal of EPM is to filter out "ineffective" or "spammy" actions to provide a more accurate measure of a player's meaningful activity. EPM is also recorded for each second of the game.

The current EPM calculation logic includes the following filtering rules:

*   **Redundant Commands:** Commands that are identical to the immediately preceding command (same event type, same ability name) and occur within a very short time frame (currently 0.5 seconds) are considered redundant and are not counted towards EPM.

Further refinements to the EPM calculation logic may be implemented in the future to include more sophisticated filtering rules, such as handling rapid selection changes or failed commands.