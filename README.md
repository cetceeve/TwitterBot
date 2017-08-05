# TwitterBot
Website: https://github.com/cetceeve/TwitterBot

### Analysieren und Visualisieren von Daten in Tweets

Mit diesem Programm können Sie Daten, anhand eines Hashtags, von Twitter abrufen. Es wird eine vom Nutzer festgelegte Anzahl an Tweets verarbeitet.
Die Darstellung der Informationen in drei Diagrammen, bietet eine schnelle Auskunft über den Kontext des gesuchten Hashtags ('Cluster'), über die fünf Länder in denen der Hashtag besonders häufig verwendet wurde ('Origin') und darüber, wie viel der Hashtag in den letzten sieben Tagen verwendet wurde ('Performance').

### Bedienung:

- Starten des Programmes:
Mit dem Befehl `python index.py` in einem Terminal innerhalb des Programmordners starten sie das Programm.
- Ein GUI führt Sie durch die Authentifizierung beim Twitter Server
> Hinweis: Sie benötigen einen Twitter Account.

- Sie können nach jedem x-beliebigen Hashtag suchen, allerdings liefern unsere Plots bei sehr gefragten Hashtags, wie z.B. #trump keine besonders interessanten Ergebnisse, da oft alle Tweets innerhalb der letzten paar Stunden und in der gleichen Location abgeschickt wurden.
> Probieren Sie ruhig auch einmal ungewöhnlichere Hashtags, diese liefern oft schönere Ergebnisse.

- Bei der Anzahl der Tweets empfehlen wir etwa 1000, wenn nötig können bis zu 5000 Tweets geladen werden.

### Installation:

Sie benötigen eine Version von _Python 2.7_ und folgende Packages:

- numpy
- Tkinter
- matplotlib
- oauth2
- tweepy

### Struktur:

- Hauptprogramm: `index.py`
- API: `api.py`
- Visualisierung: `visual.py`

### Troubleshooting:

- **Das Programm lädt aber zeigt "Keine Rückmeldung":**
Das ist normal. Leider benötigt es noch viel Zeit, um alle Daten zu sammeln und zu verarbeiten.
> Ladezeiten bis zu drei Minuten sind nicht ungewöhnlich.

- **Das Programm funktioniert wirklich nicht:**
Falls das Programm abstürzt wird normalerweise eine Fehlermeldung im Terminal erscheinen.
Diese ist meist äußerst hilfreich. Sie können das Programm dann durch drücken von `strg + c` im Terminal beenden.
> Eine typische Fehlermeldung enthält den Error Code 429.
Das bedeutet, dass Sie zu viele Anfragen an den Twitter Server gestellt haben und nun einige Minuten warten müssen.

- **Auf der "Erdkugel" wird nichts gezeigt:**
Das ist normal. Leider sind Geographischen Daten bei Twitter nur sehr sporadisch vorhanden. Der 3D Plot ist also im Moment eher eine Tech Demo, als ein "echter" Plot.
> Meist zeigt der 3D Plot nur Beispieldaten um zu demonstrieren wie er funktionieren könnte, wenn ein geeigneter Datensatz verfügbar wäre.
