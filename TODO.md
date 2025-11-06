# TODO

## Code architecture

- The code architecture should be designed to allow for easy addition of additional anti-cheat rules, ensuring that each implementation of the rules does not conflict with others.
- Standardize the naming convention for rule files in `analyzer/rules/` to `_vX_Y` (e.g., `_v1_0`).

## Features

- Applications should be accessible locally via command lines. 
- Applications should be accessible locally via a simple graphical interface.
- The application should be able to be operated remotely via the HTTP/HTTPS protocol.
- Implement the anti-cheat rules described in the `docs/detection_procedures/` directory.
- Implemented `unnatural_camera_movement` rule.
- Implemented `selection_of_unseen_units` rule.
- Implemented `camera_movement_to_unseen_enemy` rule.
- Plan to implement multi-language support (internationalization - i18n).


