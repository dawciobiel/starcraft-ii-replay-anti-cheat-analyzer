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
- Ten długi numer to **zakodowana wersja krótkiego toonId + realmId + regionId**.  
- Battle.net używa wewnętrznego algorytmu, który łączy te wartości w jeden 64‑bitowy integer.  
- Struktura wygląda mniej więcej tak (uproszczony schemat):

```
GUID = (regionId << 60) + (realmId << 48) + toonId
```

- `<<` oznacza przesunięcie bitowe w lewo.  
- Dzięki temu każdy profil w całym Battle.net ma **unikalny globalny numer**, nawet jeśli toonId powtarza się w różnych regionach.  

---

## 📌 Przykład
Dane z replaya:
- `regionId = 2` (Europa)  
- `realmId = 1`  
- `toonId = 3744144`  

Obliczenie (uproszczone):
```
GUID = (2 << 60) + (1 << 48) + 3744144
GUID ≈ 18044323943224967168
```

I to właśnie jest ten długi numer, który widzisz w URI z klienta.

---

## ✨ Podsumowanie
- **Replay → krótkie toonId** (np. `3744144`)  
- **Battle.net klient → globalny GUID** (np. `18044323943224967168`)  
- Oba odnoszą się do tego samego profilu, ale w różnych przestrzeniach identyfikacyjnych.  
- **URL** wymaga krótkiego toonId + realmId.  
- **URI** może używać globalnego GUID.  

---
