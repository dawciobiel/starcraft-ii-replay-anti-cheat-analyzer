# Wymagania dotyczące interfejsu użytkownika (Web UI)

## 1. Docelowi użytkownicy
Zwykli gracze.

## 2. Środowisko uruchomieniowe
*   Przeglądarka internetowa (aplikacja hostowana lokalnie).

## 3. Złożoność interfejsu i wymagane elementy

Interfejs powinien być raczej złożony i zawierać następujące elementy:

### a) Formularz wyboru pliku replay
*   **[Zaimplementowane]** Pole do wskazania pliku `.SC2Replay`.
*   **[Do zrobienia]** Opcje wyboru: "Analiza" i "Wizualizacja" (domyślnie obie zaznaczone).

### b) Informacje o replayu
*   **[Zaimplementowane]** **Tabela "Drużyny":**
    *   Lista graczy w każdej drużynie.
*   **[Zaimplementowane]** **Lista graczy:**
    *   ID w grze
    *   Nick
    *   Toon ID
    *   URL Battle.net

### c) Statystyki graczy w meczu
*   **[Zaimplementowane]** ID gracza
*   **[Zaimplementowane]** Nick
*   **[Zaimplementowane]** Średnia wartość APM w całym meczu
*   **[Zaimplementowane]** Średnia wartość EPM w całym meczu
*   **[Zaimplementowane]** Łączna ilość wybudowanych robotników [SCV / drone / probe]
*   **[Zaimplementowane]** Ilość wybudowanych jednostek bojowych w czasie całego meczu
*   **[Do zrobienia]** Ilość zniszczonych jednostek wroga w czasie całego meczu
*   **[Zaimplementowane]** Ilość wybudowanych budynków w czasie całego meczu
*   **[Do zrobienia]** Ilość zniszczonych jednostek wroga w czasie całego meczu
*   **[Zaimplementowane (tymczasowo wyłączone)]** **Build order poszczególnych graczy w ciągu całego meczu:**
    *   Time in seconds
    *   Action (builded unit or stucture or started researching upgrade)
    *   **[Do zrobienia]** Own supply limit of units
*   **Wykresy:**
    *   **[Zaimplementowane]** Army Value [value / elapsed game time]
    *   **[Zaimplementowane]** Workers active / Elapsed game time
    *   **[Zaimplementowane]** Resource collection rate [Resource collection rate / Elapsed game time]
    *   **[Do zrobienia]** Upgrade spending [upgrade spending / elapsed game time]

## 4. Dostępność danych
Do zastanowienia.

## 5. Wymagania dotyczące instalacji
*   Uruchomienie lokalnego serwera Flask.

## 6. Możliwości wizualizacji
*   Na chwilę obecną generowanie statycznych obrazków PNG z wykresami.
*   W przyszłości na pewno stworzymy interaktywne mapy.

## 7. Skalowalność i dostępność
*   **Wyjaśnienie pytania:** Chodzi o to, czy w przyszłości aplikacja ma być dostępna dla wielu użytkowników jednocześnie (np. jako usługa online), czy raczej będzie to narzędzie dla pojedynczych osób, uruchamiane lokalnie na ich komputerach. Ma to wpływ na wybór architektury (np. czy potrzebujemy serwera, bazy danych dostępnej dla wielu użytkowników).
*   **Odpowiedź:** Obecnie aplikacja jest narzędziem dla pojedynczych osób, uruchamianym lokalnie.

## 8. Doświadczenie i preferencje
*   **Python:** Bardzo małe doświadczenie z Pythonem i małe z PyQt. Uważasz, że to bardzo łatwe języki. Aplikacja desktopowa byłaby bardzo lekka.
*   **Java:** Bardzo duże doświadczenie z Java, JavaFX, Java EE, Java Spring Boot. Aplikacja desktopowa nie byłaby ciężka. Dużo kodu boilerplate w Javie. Aplikacja WWW w Javie to dużo kodu i ciężko o darmowy serwer. Z Javą jest sporo roboty, choć jest kusząca.
*   **Preferencje ogólne:** Python jest łatwiejszy, co może zachęcić więcej osób do udziału w projekcie open-source.

## Propozycja technologii
*   **Flask:** Wybrano lekki framework webowy Flask do stworzenia interfejsu użytkownika.
