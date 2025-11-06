# Wymagania dotyczące interfejsu graficznego (GUI)

## 1. Docelowi użytkownicy
Zwykli gracze.

## 2. Środowisko uruchomieniowe
*   Windows 10, Windows 11
*   Linux x64 (KDE lub GNOME)

## 3. Złożoność interfejsu i wymagane elementy

Interfejs powinien być raczej złożony i zawierać następujące elementy:

### a) Formularz wyboru pliku replay
*   Pole do wskazania pliku `.SC2Replay`.
*   Opcje wyboru: "Analiza" i "Wizualizacja" (domyślnie obie zaznaczone).

### b) Informacje o replayu
*   **Tabela "Drużyny":**
    *   Lista graczy w każdej drużynie.
*   **Lista graczy:**
    *   ID w grze
    *   Nick
    *   Toon ID
    *   URL Battle.net
    *   Przykład: `1, DevNULL, 3744144, https://starcraft2.com/en-us/profile/2/1/3744144`

### c) Statystyki graczy w meczu
*   ID gracza
*   Nick
*   Średnia wartość APM w całym meczu
*   Średnia wartość EPM w całym meczu
*   Łączna ilość wybudowanych robotników [SCV / drone / probe]
*   Ilość wybudowanych jednostek bojowych w czasie całego meczu
*   Ilość zniszczonych jednostek wroga w czasie całego meczu
*   Ilość wybudowanych budynków w czasie całego meczu
*   Ilość zniszczonych jednostek wroga w czasie całego meczu
*   **Build order poszczególnych graczy w ciągu całego meczu:**
    *   Time in seconds
    *   Action (builded unit or stucture or started researching upgrade)
    *   Own supply limit of units
*   **Wykresy:**
    *   Army Value [value / elapsed game time]
    *   Workers active / Elapsed game time
    *   Resource collection rate [Resource collection rate / Elapsed game time]
    *   Upgrade spending [upgrade spending / elapsed game time]

## 4. Dostępność danych
Do zastanowienia.

## 5. Wymagania dotyczące instalacji
Do zastanowienia się nad wyborem technologii.

## 6. Możliwości wizualizacji
*   Na chwilę obecną generowanie tych obrazków, które generujemy.
*   W przyszłości na pewno stworzymy interaktywne mapy.

## 7. Skalowalność i dostępność
*   **Wyjaśnienie pytania:** Chodzi o to, czy w przyszłości aplikacja ma być dostępna dla wielu użytkowników jednocześnie (np. jako usługa online), czy raczej będzie to narzędzie dla pojedynczych osób, uruchamiane lokalnie na ich komputerach. Ma to wpływ na wybór architektury (np. czy potrzebujemy serwera, bazy danych dostępnej dla wielu użytkowników).
*   **Odpowiedź:** Do dalszego przemyślenia.

## 8. Doświadczenie i preferencje
*   **Python:** Bardzo małe doświadczenie z Pythonem i małe z PyQt. Uważasz, że to bardzo łatwe języki. Aplikacja desktopowa byłaby bardzo lekka.
*   **Java:** Bardzo duże doświadczenie z Java, JavaFX, Java EE, Java Spring Boot. Aplikacja desktopowa nie byłaby ciężka. Dużo kodu boilerplate w Javie. Aplikacja WWW w Javie to dużo kodu i ciężko o darmowy serwer. Z Javą jest sporo roboty, choć jest kusząca.
*   **Preferencje ogólne:** Python jest łatwiejszy, co może zachęcić więcej osób do udziału w projekcie open-source.

## Propozycja technologii GUI
*   **PyQt:** Najlepszy wybór ze względu na cross-platformowość, bogaty zestaw widżetów, integrację z Pythonem i wydajność.
