#!/usr/local/bin/env python
# -*- coding: utf-8 -*-
import api as twitter
import visual
import numpy as np
import re
from collections import OrderedDict
from Tkinter import *
import ast

# ------------  Need a LOT of cleaning  ------------- #


# TODO: - Fix connection while retrying to connect correctly
#       - add custom amount of searched tweets
#       - only show top 5 countries tweeting


# returns updated HashtagDic using content of one tweet
def getHashtags(searchStr, dic):
    # regEx search for hastags in Tweets
    # 'hashtags' = list of found hashtags
    hashtags = re.findall('#\S+', searchStr)
    # iterate through found hashtags
    for pos in hashtags:
        if pos in dic:
            dic.update({pos: dic[pos] + 1})
        else:
            dic.update({pos: 1})
    return dic


# same as above (without regEx)
def getCountry(country, countDic):
    if country in countDic:
        countDic.update({country: countDic[country] + 1})
    else:
        countDic.update({country: 1})
    return countDic


# same as above
def timestamp(searchStr, Hourdic):
    # find current day/hour using regEx
    day = str(re.findall('^\w{2,3}', searchStr))[2:-2]
    hour = int(str(re.findall('\s\d{2}[:]', searchStr))[2:-3])

    # add +1 tweet to found hour of found day
    Hourdic[day][hour] = Hourdic[day][hour] + 1

    return Hourdic


##try again old token used?

def getAuth():
    global token
    pin = PinEntry.get()
    if twitter.getToken(pin, token):
        authent.set("Authentication successful - please enter the hashtag to search for and press 'Search'")
        TryAgB.pack_forget()
        Auth.config(fg = "green")
        Auth.pack()
        HashtagEntry.pack()
        SearchB.pack()
        OKButton.config(state = DISABLED)
    else:
        authent.set("Authentication failed - try again?")
        Auth.config(fg = "red")
        Auth.pack()
        TryAgB.pack()

def tryAgain():
    global token
    TryAgB.pack_forget()
    Auth.pack_forget()
    Link, token = twitter.getAuthLink()
    link.set(Link)

def startSearch():
    print len(HashtagEntry.get())
    if len(HashtagEntry.get()) != 0:
        tweets = twitter.getTweetsByHashtag(HashtagEntry.get())
        calcDisplayVis(tweets,HashtagEntry.get())
    else:
        NoHashtag.pack()

# API
#link, token = twitter.getAuthLink()
#pin = input(link + ' : ')
#if twitter.getToken(pin, token):
#    tweets = twitter.getTweetsByHashtag('nog20p')

# ####TESTTWEETS  Delete later
#tweets = [{"text": "#abc #def lol", "username": "test", "timestamp": "Thu Jul 06 19:37:36 +0000 2017", "geo": "de"},
          #{"text": "#abcd #abc", "username": "testtest", "timestamp": "Thu Jul 06 20:37:36 +0000 2017", "geo": "gb"}]
################
def calcDisplayVis(tweets,searchedHash):
    # create empty dicts to be filled later
    # should dicts be to slow use sets
    HashtagDic = {}
    CountryDic = {}
    # ordered Dic (Weekday order is important)
    TimeDic = OrderedDict()

    coordList = list()
    # creating weekdays and filling every hour with '0' tweets
    # (to be edited later)
    for x in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        TimeDic.update({x: {0: 0}})
        for y in range(0, 24):
            TimeDic[x][y] = 0


            # iterate through every tweetList
    for tweet in tweets:
        for key in tweet:
            if key == "text":
                # creates a dic: 'HashtagName' : 'HashtagCount'
                HashtagDic = getHashtags(tweet["text"], HashtagDic)
            if key == "geo":
                    # creates a dic 'Countries' : 'countryCount'
                CountryDic = getCountry(tweet["geo"], CountryDic)
            if key == "coordinates":
                if tweet["coordinates"] != "0":
                    coordList.append(ast.literal_eval(tweet["coordinates"]))
            if key == "timestamp":
                        # create a dict in a dict:
                        # Weekdays as keys : (Hour of the day : tweetCount)
                TimeDic = timestamp(tweet["timestamp"], TimeDic)

                        # write every Dict in a npArray to give to visual

    hashtags = list()
    hashtagNumbers = list()
    count = 0
    HashtagDic.pop("#"+searchedHash)
    for x in sorted(HashtagDic, key=HashtagDic.get, reverse=True):
        hashtags.append(x)
        hashtagNumbers.append(HashtagDic[x])
        count += 1;
        if count == 5:
            break

    Countries = np.asarray(CountryDic.keys())
    countryCount = np.asarray(CountryDic.values())

    Days = np.asarray(TimeDic.keys())
                        # create a empty list to write the tweetCounts of every hour of every day in order into ONE List
                        # then create a npArray of the list
    Hours = []
    for key in TimeDic:
        Hours.append(TimeDic[key].values())
        Hourlist = np.asarray(sum(Hours, []))

    # Visualisierung
    # Instatiert ein Visual-Object, Initiert das Fenster
    # kein input
    vis = visual.Visual()

# Plot zeigt andere Hashtags die oft zusammen mit dem gesuchten Hashtag geschrieben wurden
# Für-einen-Datenpunkt:
# auf Platz1 stehen die Hashtags
# auf Platz2 steht die Zahl, wie oft ein Hashtag zusammen mit dem gesuchten Hashtag gefunden wurde
# Input: Platz1: List of Strings, Platz2: List of Integers
    vis.barplot(np.asarray(hashtags),np.asarray(hashtagNumbers))

# Plot zeigt aus welchem Land die Tweets mit dem gesuchten Hashtag kommen
# Für-einen-Datenpunkt:
# auf Platz1 stehen die Namen der Länder
# auf Platz2 steht die Zahl der Tweets aus dem zugehörigen Land
# Input: Platz1: List of Strings, Platz2: List of Integers
    vis.piechart(Countries, countryCount)

# Plot zeigt die Gesamtzahl von Tweets im zeitlichen Verlauf der letzten 7 Tage
# Für-einen-Datenpunkt:
# auf Platz1 stehen die Wochentage mit zwei Buchstaben also 'Mo', 'Di', usw.
# auf Platz2 steht die Anzahl der Tweets innerhalb einer Stunde!
# Input: Platz1: List of Strings, Platz2: List of Integers
    vis.scatterplot(Days, Hourlist)

# Plot zeigt die Welt und die genaue Position der Tweets in 3D
# Als Dataset werden etwa 1000 Koordinatenpunkte <<[Breitengrad, Längengrad]>> benötigt
# Input: 2D Array of floats <<np.asarray([[0,0],[0,180]])>>
    print(repr(coordList))
    vis.globalscatter(np.asarray(coordList))

# Zeigt das Fenster mit allen Plots
# !wartet bis das Plotfenster geschlossen wird!
# kein input
    vis.display()

#####----------APP START--------------#####
# UI #
root = Tk()
root.width = 150
instr1 = StringVar()
instr2 = StringVar()
noHash = StringVar()
authent = StringVar()
link = StringVar()
instr2.set("Please enter the pin below and press 'OK'")
instr1.set("Use this link to get an authentication pin:")
noHash.set("No hashtag entered")

Link, token = twitter.getAuthLink()
link.set(Link)

#labels
label1 = Label(root, textvariable=instr1)
label2 = Label(root, textvariable=instr2)
NoHashtag = Label(root, textvariable=noHash)
Auth = Label(root, textvariable = authent)

#Entries
LinkEntry = Entry(root,textvariable=link,width = 90, state="readonly")
PinEntry = Entry(root, width = 20)
HashtagEntry = Entry(root, width = 30)
#Buttons
OKButton = Button(root, text ="OK", command = getAuth)
SearchB = Button(root, text="Search!", command = startSearch)
TryAgB = Button(root, text="Try Again!", command = tryAgain)

label1.pack()
LinkEntry.pack()
label2.pack()
PinEntry.pack()
OKButton.pack()

root.mainloop()
