# Twitteranalyse

### Analysieren und Visualisieren von Daten in Tweets

- Programm zur Visualisierung von Daten in Tweets
- Nutzer kann über eine Maske ein Stichwort festlegen
- Programm geht rückwirkend alle Tweets in einem Zeitraum durch und verarbeitet diejenigen, welche das Stichwort beinhalten
- Anschließend werden dem Nutzer verschiedene Daten (wie z. B. Menge und Ort) zu den verarbeiteten Tweets dargestellt

### Aufgabenverteilung:

- _API:_ Felix
- _Verarbeitung:_ Anna-Lena
- _Visulalisierung:_ Fabian

### Struktur:
Hauptprogramm + API + Visualisierung

### 1. Funktion:
- 1 hashtag suchen
- Tweets mit Metadaten der letzten 7 Tage sammeln
- Visualisierung:
  - Menge pro Tag (Histogramm; Menge über Tag)
  - Top 5 Länder (Kreisdiagramm)
  - Hashtagverbindungen (top 5 der hashtags die zusammen mit dem gesuchten genannt werden)

### API Usage

```python
import api as twitter

#Gib einen vorläufigen Token und den Link zur Authentifizierung zurück
link, token = twitter.getAuthLink()

#TODO: Hier muss ein Fenster den Link anzeigen und den Pin abfragen
twitter.getToken(user_pin, token)

#Anschließend kann die API benutzt werden, es wird ein Objekt übergeben, dass die erwarteten Rückgabewerte beschreibt
tweets = twitter.getTweetsbyHashtag({'geo' = True, timestamp = True, username = False})
# => tweets -> [['text': 'abc', 'username': 'test', 'timestamp': 123456, 'geo': 'de'], [...], ...]
```
