Instrukcje dla Gemini:
- Komunikuj się w języku polskim.
- Kod i komentarze w kodzie twórz w języku angielskim.

Podsumowanie sesji z dnia 31 października 2025:
- Skonfigurowano środowisko i zainstalowano zależności.
- Naprawiono następujące błędy w `parser/parser.py`:
    - `sqlite3.ProgrammingError: Error binding parameter 4: type 'Team' is not supported` -> Naprawiono poprzez użycie `player.team.number`.
    - `sqlite3.OperationalError: table players already exists` -> Naprawiono poprzez usunięcie `replay_data.db` na początku `init_db`.
    - `AttributeError: 'Unit' object has no attribute 'x'` -> Naprawiono poprzez użycie `event.unit.location[0]` i `event.unit.location[1]`.
    - `sqlite3.ProgrammingError: Incorrect number of bindings supplied` -> Naprawiono poprzez skorygowanie argumentów dla wstawiania `structures`.
    - `AttributeError: 'NoneType' object has no attribute 'pid'` -> Naprawiono poprzez dodanie sprawdzenia `event.unit.owner` dla `structures` i `units`.
    - `AttributeError: 'Unit' object has no attribute 'health'` -> Naprawiono poprzez użycie `getattr(event.unit, "health", None)`.
- Pomyślnie uruchomiono `cli.py` z flagą `--analyze` na pliku `replays/game.SC2Replay`.
- Analiza pliku `replays/game.SC2Replay` nie wygenerowała żadnych alertów.

Podsumowanie sesji z dnia 2 listopada 2025:
- Zweryfikowano parser `parser/parser.py` pod kątem poprawnego wczytywania danych z pliku replay'a `replays/1v1_TvP.SC2Replay`.
- Naprawiono następujące błędy w `parser/parser.py`:
    - `sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 8, and there are 7 supplied.` -> Naprawiono poprzez dodanie `getattr(event.unit, "shield", None)` do wstawiania `units`.
    - `AttributeError: 'Replay' object has no attribute 'init_data'` -> Naprawiono poprzez zmianę podejścia do pobierania początkowych jednostek.
    - `AttributeError: 'Replay' object has no attribute 'setup_units'` -> Naprawiono poprzez zmianę podejścia do pobierania początkowych jednostek.
    - `AttributeError: 'Participant' object has no attribute 'is_building'` -> Naprawiono poprzez iterowanie przez `replay.objects.values()` w celu uzyskania obiektów `Unit`.
    - `KeyError: 2` (podczas dostępu do `replay.objects[unit_id]`) -> Naprawiono poprzez iterowanie przez `replay.objects.values()` zamiast `replay.active_units`.
    - Duplikaty początkowych budynków głównych (np. dwa Nexusy) -> Naprawiono poprzez dodanie logiki sprawdzającej, czy główny budynek dla gracza został już wstawiony.
- Zaktualizowano `requirements.txt` do najnowszej wersji `sc2reader` (1.8.0).
- Parser `parser/parser.py` teraz poprawnie identyfikuje i wstawia początkowe główne budynki (po jednym na gracza) z `timeline_id = 1`.
- Naprawiono błąd braku zdarzeń kamery (`CameraEvent`) poprzez zmianę iteracji z `replay.tracker_events` na `replay.events`.

Postanowienia na przyszłość:
1. Analizowanie eventów celem wykrycia maphacka zostawiamy na sam koniec. Bo muszę dostarczyć odpowiedni replay który takiego oszusta zawiera. Poza tym musimy być pewni, że aplikacja działa poprawnie zanim zabierzemy się za tworzenie analizera eventów.
2. Muszę się zastanowić jakie informacje mogą nam być potrzebne do analizy, np.:
- współrzędne [X,Y] obiektów (budynków, jednostek, view point), 
- APM (czyli Action Peer Minute gracza - o ile w replayu ta informacja jest zawarta), 
- FPM (czyli Effective action Peer Minute - o ile w replayu ta informacja jest zawarta),
- informacje o naciskanych klawiszach na klawiaturze lub myszy (o ile takie informacje w replayu są w ogóle zawarte)
- czy w replayu jest zawarta informacja (event?) który określa, że gracz zaznaczył (kliknął) na jakąś jednostekę bądź budynek?

3. Moduł od analizowania powinien mieć strukturę modułową. Tak aby w łatwy sposób można było dodawać kolejne elementy, tzn. niezależne reguły sprawdzające ściśle określone informacje. Reguły te muszą działać niezależnie od siebie i nie mogą wpływać na swoją własną pracę. Rozumiesz o co mi chodzi - konstrukcja ma przypominać logicznie dodawane plugin'y.
Tylko powiem szczerze jeszcze nie wymyśliłem architektury jak się do tego zabrać. Ale zajmiemy się tym później.
