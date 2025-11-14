Świetnie – poniżej znajdziesz **techniczny podgląd struktury danych z pliku `.SC2Replay`** w formie tabeli oraz przykładowego JSON. To jest uogólniony schemat tego, co można parsować (np. przy użyciu bibliotek takich jak `sc2reader` w Pythonie).

---

## 📂 Główne sekcje replaya

| Sekcja              | Co zawiera                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| **Header**          | Wersja gry, czas trwania, mapa, tryb gry, data rozegrania                   |
| **Players**         | Dane o każdym graczu: nick, toon handle, race, team, kontrola AI/human      |
| **Game Events**     | Chronologiczny zapis wszystkich akcji (budowa, ruchy, czat, kamera)         |
| **Tracker Events**  | Statystyki ekonomiczne i wojskowe (minerały, gaz, supply, produkcja)        |
| **Attributes**      | Metadane: tryb gry, region, ustawienia lobby                                |
| **Chat Messages**   | Log czatu między graczami                                                   |

---

## 🧑‍💻 Struktura danych gracza (Players)

Każdy gracz ma zapisane m.in.:

- **displayName** – nick w grze (np. "Aventurier")  
- **toonHandle** – `s2profile://<regionId>/<realmId>/<toonId>`  
- **regionId** – np. `1` (US), `2` (EU), `3` (KR), `5` (CN)  
- **realmId** – zwykle `1`  
- **toonId** – unikalny numer profilu  
- **race** – Terran / Protoss / Zerg  
- **color** – kolor gracza w grze  
- **teamId** – numer drużyny (np. 1v1 → team 1 i 2)  
- **isHuman** – czy gracz to człowiek czy AI  

---

## 📊 Struktura statystyk (Tracker Events)

- **mineralsCurrent**, **vespeneCurrent** – aktualne zasoby  
- **mineralsCollectionRate**, **vespeneCollectionRate** – tempo zbierania  
- **workersActiveCount** – liczba aktywnych robotników  
- **supplyUsed**, **supplyCap** – populacja  
- **unitsProduced**, **unitsLost**, **unitsKilled**  
- **structuresBuilt**, **structuresLost**, **structuresKilled**  
- **upgradeResearched** – lista ulepszeń  

---

## 💬 Struktura czatu (Chat Messages)

- **playerId** – ID gracza wysyłającego wiadomość  
- **timestamp** – czas w grze  
- **message** – treść wiadomości  

---

## 📝 Przykładowy JSON (uproszczony)

```json
{
  "header": {
    "gameVersion": "5.0.11",
    "mapName": "Ever Dream LE",
    "gameDuration": 842,
    "regionId": 2,
    "realmId": 1
  },
  "players": [
    {
      "displayName": "Aventurier",
      "toonHandle": "s2profile://2/1/3744144",
      "regionId": 2,
      "realmId": 1,
      "toonId": 3744144,
      "race": "Protoss",
      "teamId": 1,
      "isHuman": true
    },
    {
      "displayName": "Opponent",
      "toonHandle": "s2profile://2/1/9876543",
      "regionId": 2,
      "realmId": 1,
      "toonId": 9876543,
      "race": "Zerg",
      "teamId": 2,
      "isHuman": true
    }
  ],
  "trackerEvents": [
    {
      "timestamp": 120,
      "mineralsCurrent": 300,
      "vespeneCurrent": 0,
      "supplyUsed": 14,
      "supplyCap": 15,
      "workersActiveCount": 12
    }
  ],
  "chatMessages": [
    {
      "playerId": 1,
      "timestamp": 200,
      "message": "gl hf"
    }
  ]
}
```

---

