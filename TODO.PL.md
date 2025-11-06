# TODO

## Architektura kodu

- Architektura kodu powinna być zaprojektowana w taki sposób, aby umożliwić łatwe dodawanie dodatkowych reguł anty-cheat, zapewniając, że każda implementacja reguł nie będzie kolidować z innymi.
- Standaryzuj konwencję nazewniczą dla plików reguł w `analyzer/rules/` na `_vX_Y` (np. `_v1_0`).

## Funkcjonalności

- Zaimplementowano skrypt do automatycznej aktualizacji danych o zasięgu widzenia jednostek z Liquipedii.
- Aplikacje powinny być dostępne lokalnie za pomocą linii poleceń.
- Aplikacje powinny być dostępne lokalnie za pomocą prostego interfejsu graficznego.
- Aplikacja powinna mieć możliwość zdalnej obsługi za pomocą protokołu HTTP/HTTPS.
- Zaimplementuj reguły anty-cheat opisane w katalogu `docs/detection_procedures/`.
- Zaimplementowano regułę `unnatural_camera_movement`.
- Zaimplementowano regułę `selection_of_unseen_units`.
- Zaimplementowano regułę `camera_movement_to_unseen_enemy`.
- Planowana implementacja wsparcia dla wielu języków (internacjonalizacja - i18n).
- Zaimplementowano regułę `unnatural_camera_movement`.
- Zaimplementowano regułę `selection_of_unseen_units`.
- Zaimplementowano regułę `camera_movement_to_unseen_enemy`.