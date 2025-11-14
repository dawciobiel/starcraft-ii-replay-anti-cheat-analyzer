Oto pełna tabela mapująca **regionId → region + locale**, dzięki czemu łatwo wygenerujesz poprawne **Battle.net URL** i **Battle.net URI** z danych w replayu:

---

## 🌍 Mapowanie regionów StarCraft II

| regionId | Region (nazwa) | Locale (najczęściej używane) | Przykład URL | Przykład URI |
|----------|----------------|------------------------------|--------------|--------------|
| **1**    | Ameryka Północna (US) | `en-us` | `https://starcraft2.com/en-us/profile/1/1/<toonId>` | `battlenet:://starcraft/profile/1/<toonId>` |
| **2**    | Europa (EU) | `en-gb`, `pl-pl`, `fr-fr`, `de-de` | `https://starcraft2.com/pl-pl/profile/2/1/<toonId>` | `battlenet:://starcraft/profile/2/<toonId>` |
| **3**    | Korea / Tajwan (KR/TW) | `ko-kr`, `zh-tw` | `https://starcraft2.com/ko-kr/profile/3/1/<toonId>` | `battlenet:://starcraft/profile/3/<toonId>` |
| **5**    | Chiny (CN) | `zh-cn` | `https://starcraft2.com/zh-cn/profile/5/1/<toonId>` | `battlenet:://starcraft/profile/5/<toonId>` |

---

### 📌 Uwagi praktyczne
- **realmId** – w większości przypadków jest `1`, ale replay zawsze poda właściwą wartość.  
- **toonId** – unikalny numer profilu gracza, kluczowy do budowy linku.  
- **locale** – możesz podmienić na dowolny język obsługiwany w danym regionie (np. `pl-pl` dla polskiego, `fr-fr` dla francuskiego).  
- **BattleTag** (`Nick#12345`) – jak wspomniałem wcześniej, **nie jest zapisany w replayu**.  

---



