#!/usr/local/bin/env python
# -*- coding: utf-8 -*-
# Github: https://github.com/cetceeve/TwitterBot
# Anna Lena Sporrer
# Fabian Zeiher
import api as twitter
import visual
import numpy as np
import re
from collections import OrderedDict
import Tkinter as tk
import ast


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


# OK Button after pin entry
def getAuth():
    pin = PinEntry.get()
    # check for the right pin -> success path
    if twitter.getToken(pin, token):
        authent.set("Authentication successful - please enter the hashtag to search for and press 'Search'")
        # make sure TRYAGAIN button is not visible
        TryAgB.grid_forget()
        # setup success message
        Auth.config(fg="forest green")
        Auth.grid(row=5)
        # setup search options (Hashtag entry, number entry, search button)
        Hashtag.grid(row=6, sticky=tk.W)
        HashtagEntry.grid(row=6, column=0)
        HashtagNumber.grid(row=7, sticky=tk.W)
        HashtagNumberEntry.grid(row=7, column=0)
        GeoDataCheck.grid(row=8)
        SearchB.grid(row=9)
        # Grey out OK button (it's not needed anymore)
        OKButton.config(state=tk.DISABLED)
    else:
        # Fail-Path
        # setup retry message and button
        authent.set("Authentication failed - try again?")
        Auth.config(fg="red")
        Auth.grid(row=5)
        TryAgB.grid(row=6)


# RETRY-Button
def tryAgain():
    # make sure the new token is saved GLOBALLY, so the Auth-Function uses the new token
    global token
    # reset UI, get new link -> set new Link
    TryAgB.grid_forget()
    Auth.grid_forget()
    try:
        Link, token = twitter.getAuthLink()
    except Exception:
        authent.set("Server Connection failed! Please try again.")
        Auth.config(fg="red")
        Auth.grid(row=5)
        TryAgB.grid(row=6)
    else:
        link.set(Link)


# OK-Button pressed
def startSearch():
    Error.grid_forget()
    # check whether a hashtag is entered
    if len(HashtagEntry.get()) != 0 and len(HashtagNumberEntry.get()) != 0:
        # Input is there
        # NoInput.grid_forget()
        # Check if Number is an Integer
        try:
            hashtagNumber = int(HashtagNumberEntry.get())
        # no integer entered
        except ValueError:
            error_msg.set("Please enter an integer for the amount of tweets!")
            Error.grid(row=10)
        else:
            # check if the number is too high
            if hashtagNumber > 2500:
                error_msg.set("Warning! Don't load more than 2500 tweets.")
                Error.grid(row=10)
            else:
                error_msg.set("Loading tweets...")
                Error.grid(row=10)
                root.update()
                # try loading the tweets
                try:
                    # get tweets
                    tweets = twitter.getTweetsByHashtag(HashtagEntry.get(), hashtagNumber)
                # an Error occured while loading the tweets
                except Exception:
                    Error.grid_forget()
                    error_msg.set("Search returned zero tweets. Please try again.")
                    Error.grid(row=10)
                    if twitter.API_ERROR_CODE == '429':
                        Error.grid_forget()
                        error_msg.set("Warning! You have reached the download limit. Please try again in 10 Minutes.")
                        Error.grid(row=10)
                    print "Search returned zero tweets."
                else:
                    Error.grid_forget()
                    if twitter.API_ERROR_CODE == '429':
                        error_msg.set("Warning! You have reached the Download Limit. Please try again in 10 Minutes.")
                        Error.grid(row=10)
                    root.update()
                    # analyze tweets if nothing went wrong
                    calcDisplayVis(tweets, HashtagEntry.get())

    else:
        error_msg.set("Please enter one hashtag and one number!")
        Error.grid(row=10)


# Analyze tweets
def calcDisplayVis(tweets, searchedHash):
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
            # only IF coordinates are available they are added to the list
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
    # delete first Hashtag
    HashtagDic.pop("#" + searchedHash)
    # sort used hashtags after most used hashtags and create a list of the top 5
    for x in sorted(HashtagDic, key=HashtagDic.get, reverse=True):
        hashtags.append(x)
        hashtagNumbers.append(HashtagDic[x])
        count += 1
        if count == 5:
            break

    # sort countries after the amount of tweets
    # create a list of country tags from dictionary keys
    Countries = sorted(CountryDic, key=CountryDic.__getitem__, reverse=True)
    countryCount = []
    # create list with the amount of tweets from each country
    # this list adapts the sorting from the Countries list
    for key in Countries:
        countryCount.append(CountryDic[key])

    Days = np.asarray(TimeDic.keys())
    # create a empty list to write the tweetCounts of every hour of every day in order into ONE List
    # then create a npArray of said list
    Hours = []
    for key in TimeDic:
        Hours.append(TimeDic[key].values())
        Hourlist = np.asarray(sum(Hours, []))

    # Visualisierung
    # Instatiert ein Visual-Object, Initiert das Fenster
    # kein input
    vis = visual.Visual(geoDataCheck.get())

    # Plot zeigt andere Hashtags die oft zusammen mit dem gesuchten Hashtag geschrieben wurden
    # Für-einen-Datenpunkt:
    # auf Platz1 stehen die Hashtags
    # auf Platz2 steht die Zahl, wie oft ein Hashtag zusammen mit dem gesuchten Hashtag gefunden wurde
    # Input: Platz1: List of Strings, Platz2: List of Integers
    vis.create_barplot(np.asarray(hashtags), np.asarray(hashtagNumbers))

    # Plot zeigt aus welchem Land die Tweets mit dem gesuchten Hashtag kommen
    # Für-einen-Datenpunkt:
    # auf Platz1 stehen die Namen der Länder
    # auf Platz2 steht die Zahl der Tweets aus dem zugehörigen Land
    # Input: Platz1: List of Strings, Platz2: List of Integers
    vis.create_piechart(np.asarray(Countries[:5]), np.asarray(countryCount[:5]))

    # Plot zeigt die Gesamtzahl von Tweets im zeitlichen Verlauf der letzten 7 Tage
    # Für-einen-Datenpunkt:
    # auf Platz1 stehen die Wochentage mit zwei Buchstaben also 'Mo', 'Di', usw.
    # auf Platz2 steht die Anzahl der Tweets innerhalb einer Stunde!
    # Input: Platz1: List of Strings, Platz2: List of Integers
    vis.create_scatterplot(Days, Hourlist)

    # Plot zeigt die Welt und die genaue Position der Tweets in 3D
    # Als Dataset werden etwa 1000 Koordinatenpunkte <<[Breitengrad, Längengrad]>> benötigt
    # Input: 2D Array of floats <<np.asarray([[0,0],[0,180]])>>
    #    print(repr(np.asarray(coordList)))
    if geoDataCheck.get():
        if not coordList:
            vis.create_globalscatter()
        else:
            vis.create_globalscatter(np.asarray(coordList), 1)

    # Zeigt das Fenster mit allen Plots
    # !wartet bis das Plotfenster geschlossen wird!
    # kein input
    vis.display()


# ##########-----------------APP START-------------------##########
# UI #
# create window
root = tk.Tk()
root.width = 150
# create textvariables
instr1 = tk.StringVar()
instr2 = tk.StringVar()
authent = tk.StringVar()
link = tk.StringVar()
hashNum = tk.StringVar()
Hash = tk.StringVar()
error_msg = tk.StringVar()

# create other variables
geoDataCheck = tk.BooleanVar()

# edit textvariables
instr2.set("Please enter the pin below and press 'OK'")
instr1.set("Use this link to get an authentication pin:")
hashNum.set("Tweets Number:")
Hash.set("Hashtag (without \"#\") :")

# create labels
label1 = tk.Label(root, textvariable=instr1)
label2 = tk.Label(root, textvariable=instr2)
Error = tk.Label(root, textvariable=error_msg, fg="red")
Auth = tk.Label(root, textvariable=authent)
Hashtag = tk.Label(root, textvariable=Hash)
HashtagNumber = tk.Label(root, textvariable=hashNum)

# create Entries
LinkEntry = tk.Entry(root, textvariable=link, width=90, state="readonly")
PinEntry = tk.Entry(root, width=20)
HashtagEntry = tk.Entry(root, width=30)
HashtagNumberEntry = tk.Entry(root, width=30)

# create Buttons
OKButton = tk.Button(root, text="OK", command=lambda: getAuth())
SearchB = tk.Button(root, text="Search!", command=startSearch)
TryAgB = tk.Button(root, text="Try Again!", command=lambda: tryAgain())

# create Checkbutton
GeoDataCheck = tk.Checkbutton(root, text="Display GeoData in 3D Plot", variable=geoDataCheck, onvalue=True, offvalue=False)

# setup starting window
label1.grid(row=0)
LinkEntry.grid(row=1)
label2.grid(row=2)
PinEntry.grid(row=3)
OKButton.grid(row=4)

# get a new link/token
try:
    Link, token = twitter.getAuthLink()
except Exception:
    authent.set("Server Connection failed! Please try again.")
    Auth.config(fg="red")
    Auth.grid(row=5)
    TryAgB.grid(row=6)
else:
    link.set(Link)

# start mainloop
root.mainloop()
