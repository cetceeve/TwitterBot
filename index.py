#!/usr/bin/env python
# -*- coding: utf-8 -*-
import api as twitter
import visual

#API
#link, token = twitter.getAuthLink()
#pin = input(link + ' : ')
#if twitter.getToken(pin, token):
#    print twitter.getTweetsByHashtag('nog20p')

#Visualisierung
#Instatiert ein Visual-Object, Initiert das Fenster
#kein input
vis = visual.Visual()

# Plot zeigt andere Hashtags die oft zusammen mit dem gesuchten Hashtag geschrieben wurden
#Für-einen-Datenpunkt:
# auf Platz1 stehen die Hashtags
# auf Platz2 steht die Zahl, wie oft ein Hashtag zusammen mit dem gesuchten Hashtag gefunden wurde
#Input: Platz1: List of Strings, Platz2: List of Integers
vis.barplot()

# Plot zeigt aus welchem Land die Tweets mit dem gesuchten Hashtag kommen
#Für-einen-Datenpunkt:
# auf Platz1 stehen die Namen der Länder
# auf Platz2 steht die Zahl der Tweets aus dem zugehörigen Land
#Input: Platz1: List of Strings, Platz2: List of Integers
vis.piechart()

# Plot zeigt die Gesamtzahl von Tweets im zeitlichen Verlauf der letzten 7 Tage
#Für-einen-Datenpunkt:
# auf Platz1 stehen die Wochentage mit zwei Buchstaben also 'Mo', 'Di', usw.
# auf Platz2 steht die Anzahl der Tweets innerhalb einer Stunde!
#Input: Platz1: List of Strings, Platz2: List of Integers
vis.scatterplot()

# Plot zeigt die Welt und die genaue Position der Tweets in 3D
# Als Dataset werden etwa 1000 Koordinatenpunkte <<[Breitengrad, Längengrad]>> benötigt
#Input: 2D Array of floats <<np.asarray([[0,0],[0,180]])>>
vis.globalscatter()

#Zeigt das Fenster mit allen Plots
#!wartet bis das Plotfenster geschlossen wird!
#kein input
vis.display()

