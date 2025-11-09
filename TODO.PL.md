# TODO

## Architektura kodu
- [x] Refaktoryzacja logiki biznesowej do oddzielnego modułu `core`.
- [x] Wersjonowanie parsera i schematu bazy danych.
- [x] Przeniesienie kosztów jednostek i ulepszeń do pliku konfiguracyjnego.
- [ ] Zastanów się nad ewentualnym użyciem Nuitka w celu ochrony kodu źródłowego.
- [ ] Wybierz odpowiednią licencję dla projektu.

## Funkcjonalności
- [x] Implementacja interfejsu webowego (Flask) do analizy powtórek.
- [x] Rozbudowa interfejsu webowego o pozostałe statystyki i wykresy.
- [x] Implementacja brakujących statystyk (np. "ilość zniszczonych jednostek wroga").
- [x] Implementacja brakujących wykresów (np. "wydatki na ulepszenia").
- [x] Dodanie opcji wyboru "Analiza" i "Wizualizacja" w formularzu przesyłania.
- [ ] Aplikacja powinna mieć możliwość zdalnej obsługi za pomocą protokołu HTTP/HTTPS.
- [x] Zaimplementuj reguły anty-cheat opisane w katalogu `docs/detection_procedures/`.
