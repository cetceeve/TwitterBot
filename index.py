#!/usr/local/bin/env python
# -*- coding: utf-8 -*-
# Github: https://github.com/cetceeve/TwitterBot
# Anna Lena Sporrer
# Fabian Zeiher
import api as twitter
import visual
import gui
import threading
import Queue
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
def getAuth(event):
    pin = ui.entry_auth_pin.get()
    # check for the right pin -> success path
    if twitter.getToken(pin, token):
        # make sure TRYAGAIN button is not visible
        ui.clear_tryagain()
        # display serch area
        ui.display_search()
    else:
        # Fail-Path
        # setup retry message and button
        ui.authentication_error()


# RETRY-Button
def tryAgain(event):
    # make sure the new token is saved GLOBALLY, so the Auth-Function uses the new token
    global token
    # reset UI, get new link -> set new link
    ui.clear_tryagain()
    try:
        auth_link, token = twitter.getAuthLink()
    except Exception:
        ui.server_connection_error()
    else:
        ui.string_auth_link.set(auth_link)


# OK-Button pressed
def startSearch(event):
    # check whether a hashtag is entered
    if len(ui.entry_search_hashtag.get()) != 0 and len(ui.entry_search_amountoftweets.get()) != 0:
        # Check if Number is an Integer
        try:
            hashtagNumber = int(ui.entry_search_amountoftweets.get())
        # no integer entered
        except ValueError:
            ui.info_message("Please enter an integer for the amount of tweets!")
        else:
            # check if the number is too high
            if hashtagNumber > 2500:
                ui.info_message("Warning! Don't load more than 2500 tweets.")
            else:
                # try loading the tweets
                try:
                    # get tweets
                    searchHashtag = ui.entry_search_hashtag.get()
                    qu1 = Queue.Queue()
                    qu2 = Queue.Queue()
                    qu3 = Queue.Queue()
                    background_thread = threading.Thread(target=twitter.getTweetsByHashtag,
                                                         args=(searchHashtag, hashtagNumber, qu1, qu2, qu3))
                    background_thread.start()
                    print "open background thread"
                    runner = 0
                    while runner < hashtagNumber:
                        runner = qu2.get()
                        ui.info_message('Loading: {}/{}'.format(runner, hashtagNumber), 'blue')
                        root.update()
                    trueAmount = qu3.get()
                    tweets = qu1.get()
                    background_thread.join()
                    print "close background thread"
                    if not tweets:
                        raise Exception("Search returned zero tweets. Please try again.")
                # an Error occured while loading the tweets
                except Exception as e:
                    if twitter.API_ERROR_CODE == '000':
                        ui.info_message(e, 'blue')
                        print "Search returned zero tweets."
                    elif twitter.API_ERROR_CODE == '429':
                        ui.info_message("Warning! You have reached the download limit. Please try again in 10 Minutes.")
                    else:
                        ui.info_message("Error! Something went wrong while trying to load the tweets.")
                    root.update()
                else:
                    ui.info_message("Successfully finished loading! {} tweets were found.".format(trueAmount), 'forest green')
                    if twitter.API_ERROR_CODE == '429':
                        ui.info_message(
                            "Warning! You have reached the Download Limit. Loaded {} tweets successfully.".format(trueAmount), 'orange')
                    elif twitter.API_ERROR_CODE != '000':
                        ui.info_message("Warning! Something went wrong. Loaded {} tweets successfully.".format(trueAmount), 'orange')
                    root.update()
                    # analyze tweets if nothing went wrong
                    calcDisplayVis(tweets, ui.entry_search_hashtag.get())

    else:
        ui.info_message("Please enter one hashtag and one number!")


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

    # error can be thrown because the api is not case sensitive but we are
    try:
        # delete first Hashtag
        HashtagDic.pop("#" + searchedHash)
    except KeyError:
        # leave it as is
        pass

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
    vis = visual.Visual(ui.boolean_geodatacheck.get())

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
    if ui.boolean_geodatacheck.get():
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
root.title("TwitterBot")
# initialize ui object
ui = gui.App(root)
# keybindings
ui.button_auth_ok.bind("<Button-1>", getAuth)
ui.button_auth_tryag.bind("<Button-1>", tryAgain)
ui.button_search.bind("<Button-1>", startSearch)
# starting screen
ui.display_auth()

try:
    auth_link, token = twitter.getAuthLink()
except Exception:
    ui.server_connection_error()
else:
    ui.string_auth_link.set(auth_link)

root.mainloop()
