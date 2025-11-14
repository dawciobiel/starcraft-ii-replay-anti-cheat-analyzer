Tu wchodzimy w różnicę między tym, co **replay faktycznie zapisuje**, a tym, co jest widoczne w profilu Battle.net.  

### 🔗 Battle.net URL i URI
- **Battle.net URL** (np. `https://starcraft2.com/en-us/profile/2/1/3744144`) – można go odtworzyć z danych w replayu, bo plik zawiera **region ID**, **realm ID** i **toon ID**.  
- **Battle.net URI** (np. `battlenet:://starcraft/profile/2/18044323943224967168`) – również możliwy do wygenerowania, bo replay przechowuje te same identyfikatory w formacie używanym przez klienta Battle.net.  

### 🧑‍💻 BattleTag
- **BattleTag (np. `Aventurier#224312689`)** – tego replay **nie zapisuje wprost**.  
- W pliku znajdziesz **toon handle** (ciąg znaków typu `s2profile://...`), który pozwala zbudować URL/URI do profilu.  
- BattleTag jest **prywatnym identyfikatorem konta Battle.net** i nie jest przechowywany w replayu ze względów bezpieczeństwa.  
- Możesz go zobaczyć tylko, jeśli gracz sam udostępni swój profil Battle.net lub jeśli zalogujesz się i masz dostęp do listy znajomych.  

### 📌 Podsumowanie
Z replaya wyciągniesz:
- **Region ID, Realm ID, Toon ID**  
- **Battle.net URL i URI** (możliwe do zbudowania)  
- **Nick w grze (display name)**  

Ale **BattleTag (z numerem po #)** nie jest dostępny w replayu – to pozostaje ukryte. Replay daje ci tylko dane potrzebne do odwołania się do profilu, nie pełny identyfikator konta.  

