#!/usr/local/bin/env python
# -*- coding: utf-8 -*-
import api as twitter
import visual
import numpy as np
import re
from collections import OrderedDict

# ------------  Need a LOT of cleaning  ------------- #

#returns updated HashtagDic using content of one tweet
def getHashtags(searchStr, dic):
    hashtags =  re.findall('#\S+', searchStr)
    for pos in hashtags:
        if pos in dic:
            dic.update({pos : dic[pos]+1})
        else:
            dic.update({pos :1})
    return dic

def getCountry(country, countDic):
    if country in countDic:
        countDic.update({country : countDic[country]+1})
    else:
        countDic.update({country : 1})
    return countDic

def timestamp(searchStr,Hourdic):
    day = str(re.findall('^\w{2,3}', searchStr))[2:-2]
    hour = int(str(re.findall('\s\d{2}[:]', searchStr))[2:-3])

    #if day in Hourdic and hour in Hourdic[day]:
    Hourdic[day][hour] = Hourdic[day][hour]+1
    #else:
    #    if day not in Hourdic:
    #        Hourdic.update({day : {hour : 0}})
    #        for x in range(0,24):
    #            Hourdic[day][x] = 0
#
#        Hourdic[day][hour] = 1
    return Hourdic



#API
#link, token = twitter.getAuthLink()
#pin = input(link + ' : ')
#if twitter.getToken(pin, token):
    #tweets = twitter.getTweetsByHashtag('nog20p')

tweets = [{"text": "#abc #def lol", "username": "test", "timestamp": "Thu Jul 06 19:37:36 +0000 2017", "geo": "de"},
{"text": "#abcd #abc", "username": "testtest", "timestamp": "Thu Jul 06 20:37:36 +0000 2017", "geo": "gb"}]

HashtagDic = {}
CountryDic = {}
TimeDic = OrderedDict()
for x in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]:
    TimeDic.update({x : {0 : 0}})
    for y in range(0,24):
        TimeDic[x][y] = 0


for tweet in tweets:
    for key in tweet:
        if key == "text":
            #creates a dic: 'HashtagName' : 'HashtagCount'
            HashtagDic = getHashtags(tweet["text"],HashtagDic)
        if key == "geo":
            CountryDic = getCountry(tweet["geo"], CountryDic)
        if key == "timestamp":
            TimeDic = timestamp(tweet["timestamp"], TimeDic)


Hashtags = np.asarray(HashtagDic.keys())
HashtagNumbers = np.asarray(HashtagDic.values())

Countries = np.asarray(CountryDic.keys())
countryCount = np.asarray(CountryDic.values())

Days = np.asarray(TimeDic.keys())
Hours = []
for key in TimeDic:
    Hours.append(TimeDic[key].values())
Hourlist = np.asarray(sum(Hours, []))

#Visualisierung
#Instatiert ein Visual-Object, Initiert das Fenster
#kein input
vis = visual.Visual()

# Plot zeigt andere Hashtags die oft zusammen mit dem gesuchten Hashtag geschrieben wurden
#Für-einen-Datenpunkt:
# auf Platz1 stehen die Hashtags
# auf Platz2 steht die Zahl, wie oft ein Hashtag zusammen mit dem gesuchten Hashtag gefunden wurde
#Input: Platz1: List of Strings, Platz2: List of Integers
vis.barplot(Hashtags,HashtagNumbers)

# Plot zeigt aus welchem Land die Tweets mit dem gesuchten Hashtag kommen
#Für-einen-Datenpunkt:
# auf Platz1 stehen die Namen der Länder
# auf Platz2 steht die Zahl der Tweets aus dem zugehörigen Land
#Input: Platz1: List of Strings, Platz2: List of Integers
vis.piechart(Countries,countryCount)

# Plot zeigt die Gesamtzahl von Tweets im zeitlichen Verlauf der letzten 7 Tage
#Für-einen-Datenpunkt:
# auf Platz1 stehen die Wochentage mit zwei Buchstaben also 'Mo', 'Di', usw.
# auf Platz2 steht die Anzahl der Tweets innerhalb einer Stunde!
#Input: Platz1: List of Strings, Platz2: List of Integers
vis.scatterplot(Days, Hourlist)

# Plot zeigt die Welt und die genaue Position der Tweets in 3D
# Als Dataset werden etwa 1000 Koordinatenpunkte <<[Breitengrad, Längengrad]>> benötigt
#Input: 2D Array of floats <<np.asarray([[0,0],[0,180]])>>
#vis.globalscatter()

#Zeigt das Fenster mit allen Plots
#!wartet bis das Plotfenster geschlossen wird!
#kein input
vis.display()
