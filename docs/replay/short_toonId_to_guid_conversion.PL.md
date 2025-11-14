# Jak z krótkiego **toonId** (np. `3744144`) powstaje ten długi **GUID** (`18044323943224967168`), który widzisz w linku kopiowanym z klienta Battle.net.  

---

## 🧩 Dwa typy identyfikatorów
1. **ToonId (krótki)** – prosty numer przypisany do profilu w danym regionie/realm.  
   - Występuje w replayach i w URL do strony www (`starcraft2.com/...`).  
   - Przykład: `3744144`.  

2. **Global Toon GUID (długi)** – 64‑bitowy identyfikator używany przez aplikację Battle.net.  
   - Występuje w URI kopiowanym z klienta (`battlenet:://starcraft/profile/...`).  
   - Przykład: `18044323943224967168`.  

---

## 🔍 Jak powstaje GUID
- Ten długi numer to **zakodowana wersja krótkiego toonId + realmId + regionId**, jednak dokładny algorytm używany przez Battle.net do łączenia tych wartości w jeden 64-bitowy integer jest **proprietarny i nie jest publicznie znany**.
- Próby odtworzenia tego algorytmu na podstawie dostępnych danych z replayów nie przyniosły wiarygodnych rezultatów.
- W związku z tym, nie jest możliwe samodzielne wygenerowanie tego globalnego GUID z danych dostępnych w pliku replay.

---

## 📌 Przykład
Dane z replaya:
- `regionId = 2` (Europa)
- `realmId = 1`
- `toonId = 3744144`

**Obliczenie globalnego GUID z tych danych nie jest możliwe przy użyciu publicznie dostępnych algorytmów.**
Przykładowy GUID `18044323943224967168` jest wewnętrznym identyfikatorem Battle.net, którego nie da się odtworzyć z prostego wzoru bitowego na podstawie `regionId`, `realmId` i `toonId`.

---

## ✨ Podsumowanie
- **Replay → krótkie toonId** (np. `3744144`)
- **Battle.net klient → globalny GUID** (np. `18044323943224967168`)
- Oba odnoszą się do tego samego profilu, ale globalny GUID jest wewnętrznym identyfikatorem Battle.net, którego nie jesteśmy w stanie samodzielnie wygenerować.
- Nasza aplikacja będzie używać formatu URI opartego na `regionId`, `realmId` i `toonId` (np. `battlenet:://starcraft/profile/{regionId}/{realmId}/{toonId}`), ponieważ jest to jedyny wiarygodny sposób na konstruowanie linków z dostępnych danych.
