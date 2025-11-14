Oto **algorytm krok po kroku** w formie prostego pseudo‑kodu, który z danych `regionId`, `realmId` i `toonId` pozwala wygenerować zarówno **Battle.net URL**, jak i **Battle.net URI**:

---

## 🧮 Algorytm budowy linków

```pseudo
function buildBattleNetLinks(regionId, realmId, toonId, locale):
    # Battle.net URL
    url = "https://starcraft2.com/" + locale + "/profile/" +
          regionId + "/" + realmId + "/" + toonId

    # Battle.net URI
    # Globalny GUID nie jest możliwy do samodzielnego wyliczenia z danych replaya.
    # Używamy formatu URI opartego na regionId, realmId i toonId.
    uri = "battlenet:://starcraft/profile/" +
          regionId + "/" + realmId + "/" + toonId

    return (url, uri)
```

---

## 📌 Przykład użycia

Dane z replaya:
- `regionId = 2` (Europa)
- `realmId = 1`
- `toonId = 3744144`
- `locale = "pl-pl"`

Wynik:
- **URL** → `https://starcraft2.com/pl-pl/profile/2/1/3744144`
- **URI** → `battlenet:://starcraft/profile/2/1/3744144`

---

## 🌍 Locale (język/region strony)
- US → `en-us`
- EU → `en-gb`, `pl-pl`, `fr-fr`, `de-de`
- KR/TW → `ko-kr`, `zh-tw`
- CN → `zh-cn`

---

