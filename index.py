#!/usr/local/bin/env python
# -*- coding: utf-8 -*-
import api as twitter
import visual
import numpy as np
import re
from collections import OrderedDict

# ------------  Need a LOT of cleaning  ------------- #

#TODO: only add the ~5 most used hashtags (maybe use sets for increased speed)
#returns updated HashtagDic using content of one tweet
def getHashtags(searchStr, dic):
    #regEx search for hastags in Tweets
    #'hashtags' = list of found hashtags
    hashtags =  re.findall('#\S+', searchStr)
    #iterate through found hashtags
    for pos in hashtags:
        if pos in dic:
            dic.update({pos : dic[pos]+1})
        else:
            dic.update({pos :1})
    return dic

#same as above (without regEx)
def getCountry(country, countDic):
    if country in countDic:
        countDic.update({country : countDic[country]+1})
    else:
        countDic.update({country : 1})
    return countDic

#same as above
def timestamp(searchStr,Hourdic):
    #find current day/hour using regEx
    day = str(re.findall('^\w{2,3}', searchStr))[2:-2]
    hour = int(str(re.findall('\s\d{2}[:]', searchStr))[2:-3])

    #add +1 tweet to found hour of found day
    Hourdic[day][hour] = Hourdic[day][hour]+1

    return Hourdic



#API
#link, token = twitter.getAuthLink()
#pin = input(link + ' : ')
#if twitter.getToken(pin, token):
    #tweets = twitter.getTweetsByHashtag('nog20p')

#####TESTTWEETS  Delete later
tweets = [{"text": "#abc #def lol", "username": "test", "timestamp": "Thu Jul 06 19:37:36 +0000 2017", "geo": "de"},
{"text": "#abcd #abc", "username": "testtest", "timestamp": "Thu Jul 06 20:37:36 +0000 2017", "geo": "gb"}]
################

#create empty dicts to be filled later
#should dicts be to slow use sets
HashtagDic = {}
CountryDic = {}
#ordered Dic (Weekday order is important)
TimeDic = OrderedDict()
#creating weekdays and filling every hour with '0' tweets
#(to be edited later)
for x in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]:
    TimeDic.update({x : {0 : 0}})
    for y in range(0,24):
        TimeDic[x][y] = 0

#iterate through every tweetList
for tweet in tweets:
    for key in tweet:
        if key == "text":
            #creates a dic: 'HashtagName' : 'HashtagCount'
            HashtagDic = getHashtags(tweet["text"],HashtagDic)
        if key == "geo":
            #creates a dic 'Countries' : 'countryCount'
            CountryDic = getCountry(tweet["geo"], CountryDic)
        if key == "timestamp":
            #create a dict in a dict:
            #Weekdays as keys : (Hour of the day : tweetCount)
            TimeDic = timestamp(tweet["timestamp"], TimeDic)

#write every Dict in a npArray to give to visual
Hashtags = np.asarray(HashtagDic.keys())
HashtagNumbers = np.asarray(HashtagDic.values())

Countries = np.asarray(CountryDic.keys())
countryCount = np.asarray(CountryDic.values())

Days = np.asarray(TimeDic.keys())
#create a empty list to write the tweetCounts of every hour of every day in order into ONE List
#then create a npArray of the list
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

