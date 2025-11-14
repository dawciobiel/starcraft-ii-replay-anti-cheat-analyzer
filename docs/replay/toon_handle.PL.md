Jak z danych w replayu zbudować **Battle.net URL** i **Battle.net URI** dla profilu gracza.  

---

## 🧩 Struktura danych w replayu
W pliku `.SC2Replay` znajdziesz dla każdego gracza tzw. **toon handle**.  
Wygląda to mniej więcej tak:

```
s2profile://<regionId>/<realmId>/<toonId>
```

### Elementy:
- **regionId** – numer regionu (np. `1` = US, `2` = EU, `3` = KR, `5` = CN)  
- **realmId** – serwer w danym regionie (najczęściej `1`, ale mogą być inne)  
- **toonId** – unikalny identyfikator profilu gracza  

---

## 🔗 Battle.net URL
Format:
```
https://starcraft2.com/<locale>/profile/<regionId>/<realmId>/<toonId>
```

Przykład:
```
https://starcraft2.com/en-us/profile/2/1/3744144
```

- `locale` – język i region strony (`en-us`, `pl-pl`, `fr-fr` itd.)  
- `regionId`, `realmId`, `toonId` – bezpośrednio z replaya  

---

## 🔗 Battle.net URI
Format:
```
battlenet:://starcraft/profile/<regionId>/<toonId>
```

Przykład:
```
battlenet:://starcraft/profile/2/18044323943224967168
```

- Tutaj **realmId** nie jest używany, tylko `regionId` i `toonId`.  
- Ten URI otwiera profil bezpośrednio w aplikacji Battle.net.  

---

## 📌 Ważne ograniczenie
Replay **nie zawiera BattleTag-a** (`Nick#12345`).  
Masz tylko:
- **Display name** (nick w grze, np. "Aventurier")  
- **Toon handle** (region/realm/toonId)  

BattleTag jest prywatny i nie jest zapisywany w pliku replay – można go zobaczyć tylko w aplikacji Battle.net lub jeśli gracz sam poda link do swojego profilu.  

---

