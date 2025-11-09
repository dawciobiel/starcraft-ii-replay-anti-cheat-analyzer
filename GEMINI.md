Instrukcje dla Gemini:
- Zawsze sprawdzaj, czy środowisko pythona venv projektu jest aktywne. Jeśli nie, aktywuj je przed rozpoczęciem pracy (lub przed uruchomieniem aplikacji).
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

Podsumowanie sesji z dnia 3 listopada 2025:
- Dodano tabelę `player_apm` do schematu bazy danych w celu przechowywania danych APM i EPM.
- Zmodyfikowano parser, aby używał wtyczki `APMTracker` z `sc2reader` do pobierania danych APM.
- Zaimplementowano podstawową logikę obliczania EPM, która odfiltrowuje zbędne polecenia.
- Zapisano wartości APM i EPM w tabeli `player_apm`.
- Naprawiono błąd w schemacie tabeli `command_events`.
- Naprawiono błąd w logice obliczania EPM związany z długością gry.
- Upewniono się, że parser działa poprawnie i dane są zapisywane w bazie danych.

Podsumowanie sesji z dnia 4 listopada 2025:
- Utworzono katalog `docs` na dokumentację.
- Utworzono dokumentację dla obliczeń APM i EPM w osobnych plikach (`docs/apm_calculation.md` i `docs/epm_calculation.md`).
- Utworzono dokument z listą wszystkich danych logowanych z powtórek (`docs/logged_data_from_replay.md`).
- Przetłumaczono `TODO.md` na `TODO.PL.md`.
- Utworzono katalog `docs/detection_procedures` na dokumentację reguł anty-cheat.
- Utworzono dokumentację dla dwóch reguł anty-cheat: `unnatural_camera_movement.md` i `selection_of_unseen_units.md`.
- Zaktualizowano `TODO.md` i `TODO.PL.md`, aby wskazywały na nową dokumentację reguł anty-cheat.

Podsumowanie sesji z dnia 6 listopada 2025:
- Obecne testy należy wykonywać na replayu `replays/1v1_TvP.SC2Replay`.
- **Rozbudowa bazy danych:**
    - Dodano tabelę `control_group_events` do schematu bazy danych.
    - Zaimplementowano parsowanie zdarzeń grup kontrolnych (`SetControlGroupEvent`, `AddToControlGroupEvent`, `GetControlGroupEvent`) w `parser/parser_v1_0.py`.
    - Dodano kolumnę `z` (wysokość) do tabel `units` i `structures` w schemacie bazy danych.
    - Zaktualizowano `parser/parser_v1_0.py` do bezpiecznego zapisywania współrzędnej `z` dla jednostek i struktur.

- **Refaktoryzacja struktury plików:**
    - Przeniesiono `schema.sql` do `parser/parser_v1_0_schema.sql` i zmieniono jego nazwę.
    - Zmieniono nazwę `parser/parser.py` na `parser/parser_v1_0.py`.
    - Zaktualizowano wszystkie odwołania do tych plików w `cli.py` i `parser/parser_v1_0.py`.
    - Standaryzowano konwencję nazewniczą dla plików reguł analizatora na `_vX_Y` (np. `_v1_0`), co wymagało zmiany nazw plików i aktualizacji wewnętrznych odwołań.

- **Nowa reguła analizatora:**
    - Utworzono nową, zaawansowaną regułę `selection_of_unseen_units_with_los_v1_0.py`, która uwzględnia wysokość terenu i uproszczony model linii wzroku (LoS) do wykrywania podejrzanych zaznaczeń niewidocznych jednostek.
    - Utworzono dokumentację dla tej reguły: `docs/detection_procedures/selection_of_unseen_units_with_los_v1.0.md`.
    - Skopiowano plik `selection_of_unseen_units_v1.0.json` do katalogu nowej reguły.

- **Naprawa błędów:**
    - Naprawiono `SyntaxError` w `analyzer/rules/unnatural_camera_movement/unnatural_camera_movement_v1_0.py`.
    - Naprawiono `IndexError` w `parser/parser_v1_0.py` poprzez bezpieczne odwoływanie się do `unit.location[2]`.

- **Aktualizacja dokumentacji projektu:**
    - Zaktualizowano `GEMINI.md` o informację o używaniu `replays/1v1_TvP.SC2Replay` do testów.
    - Zaktualizowano `TODO.md` i `TODO.PL.md`, usuwając zaimplementowane zadania i odzwierciedlając decyzje dotyczące konwencji nazewniczej.

- **Testowanie:**
    - Pomyślnie przeprowadzono analizę i wizualizację na `replays/1v1_TvP.SC2Replay` oraz na `replays/to_check_is_Jesus_using_mh.SC2Replay`.
    - Replay `replays/to_check_is_Jesus_using_mh.SC2Replay` wygenerował 16 alertów, co sugeruje, że reguły działają i są w stanie wykrywać potencjalne oszustwa.

Podsumowanie sesji z dnia 6 listopada 2025 (kontynuacja):
- **Refaktoryzacja architektury analizatora:**
    - Wprowadzono klasę bazową `BaseRule` w `analyzer/analyzer.py`, która definiuje interfejs dla wszystkich reguł analizatora.
    - Wszystkie istniejące reguły analizatora zostały zmigrowane do nowej architektury opartej na klasie `BaseRule`.
    - Reguły dziedziczące z `BaseRule` są teraz odpowiedzialne za bezpośrednie wstawianie alertów do bazy danych.
    - Zaktualizowano proces wykrywania reguł w `analyzer/analyzer.py` w celu identyfikacji reguł opartych na `BaseRule`.

Podsumowanie sesji z dnia 6 listopada 2025 (kontynuacja):
- **Rozważania nad GUI:**
    - Zebrano szczegółowe wymagania dotyczące interfejsu graficznego (GUI), w tym docelowych użytkowników, środowiska uruchomieniowego, złożoności interfejsu, wymaganych elementów (formularz wyboru replaya, informacje o replayu, statystyki graczy z build orderem i wykresami).
    - Omówiono możliwości wizualizacji (obecnie statyczne obrazki, w przyszłości interaktywne mapy).
    - Przeanalizowano doświadczenie i preferencje technologiczne (Python/PyQt vs Java/JavaFX).
    - Zaproponowano PyQt jako technologię GUI ze względu na cross-platformowość, bogaty zestaw widżetów, integrację z Pythonem i wydajność.
    - Punkt dotyczący skalowalności i dostępności (wielu użytkowników vs pojedyncze osoby) został odłożony do dalszego przemyślenia.

Podsumowanie sesji z dnia 8 listopada 2025:
- **Implementacja interfejsu webowego (Flask):**
    - Stworzono aplikację webową opartą na Flask (`webapp/`).
    - Zaimplementowano przesyłanie plików `.SC2Replay`.
    - Wyświetlono podstawowe informacje o powtórce (drużyny, lista graczy).
    - Wyświetlono statystyki graczy (APM, EPM, wybudowani robotnicy, wybudowane struktury, wybudowane jednostki bojowe, zniszczone jednostki wroga).
    - Wyświetlono kolejność budowy z limitem zaopatrzenia.
    - Wyświetlono wykresy: Aktywni robotnicy, Tempo zbierania zasobów, Wartość armii, Wydatki na ulepszenia.
    - Dodano opcje interfejsu użytkownika "Analiza" i "Wizualizacja" w formularzu przesyłania.
    - Zaimplementowano zwijane sekcje dla lepszego UX.
- **Architektura:**
    - Zrefaktoryzowano logikę rdzenia do `core/analysis_service.py`.
    - Zaktualizowano `webapp/app.py` do korzystania z nowej usługi.
- **Parser i schemat:**
    - Wersjonowano pliki parsera i schematu do `v1.1`.
    - Zaktualizowano `parser/parser_v1_1.py` do przetwarzania `PlayerStatsEvent` i `UnitDiedEvent` (w tym `killer_player_id`).
    - Zaktualizowano `parser/parser_v1_1_schema.sql` o tabele `player_stats_events` i `unit_deaths`.
- **Konfiguracja:**
    - Przeniesiono koszty jednostek i ulepszeń do `config/costs.ini`.
- **Dokumentacja:**
    - Zaktualizowano `TODO.PL.md`, `docs/architecture/gui_requirements.md` i `README.md` do odzwierciedlenia bieżącego statusu projektu.
- **Poprawki błędów:**
    - Poprawiono wielkość liter `ALLOWED_EXTENSIONS` w `webapp/app.py`.
    - Poprawiono obsługę ścieżek plików w `webapp/app.py` i `core/analysis_service.py`.
    - Poprawiono `TypeError` w sygnaturze funkcji `run_full_analysis`.
    - Poprawiono `AttributeError` w `parser/parser_v1_1.py` związane z `event.killer.owner.pid`.