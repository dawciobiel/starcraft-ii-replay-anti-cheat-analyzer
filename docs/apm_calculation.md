# APM (Actions Per Minute)

APM values are retrieved directly from the `sc2reader` library, which calculates them based on all player actions (mouse clicks, key presses) within the game. The raw APM values, which are floating-point numbers, are rounded to the nearest integer before being stored in the `player_apm` table in the database. APM is recorded for each second of the game.