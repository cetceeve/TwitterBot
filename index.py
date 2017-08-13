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


# OK Button after pin entry
def get_auth(event):
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
def try_again(event):
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
def validate_input(event):
    # check if a tweet and amount are entered
    if len(ui.entry_search_hashtag.get()) == 0 and len(ui.entry_search_amountoftweets.get()) == 0:
        ui.info_message("Please enter one hashtag and the amount of tweets you want to process!")
    else:
        # store the hashtag in a variable for later use
        searchHashtag = ui.entry_search_hashtag.get()
        # Check if Number is an Integer
        try:
            # store the amount of tweets in a variable for later use
            tweetNumber = int(ui.entry_search_amountoftweets.get())
        # no integer entered
        except ValueError:
            ui.info_message("Please enter an integer for the amount of tweets!")
        # imput syntax is ok
        else:
            # check if the number is too high
            if tweetNumber > 2500:
                ui.info_message("Warning! Don't load more than 2500 tweets.")
            else:
                # ready to start loading
                load_tweets(searchHashtag, tweetNumber)


def load_tweets(searchHashtag, tweetNumber):
    # Queue objects are used to transfer data back from the background thread
    qu1 = Queue.Queue()
    qu2 = Queue.Queue()
    qu3 = Queue.Queue()
    # initialize background thread
    # the twitter.getTweetsByHashtag function will run in a background thread
    background_thread = threading.Thread(target=twitter.getTweetsByHashtag,
                                         args=(searchHashtag, tweetNumber, qu1, qu2, qu3))

    # start the background thread
    background_thread.start()
    print "open background thread"
    # runner is equal to the runner running in the background thread
    runner = 0
    # this while loop is closed from the background thread!!!
    # if the loop needs to stop queue 2 will git the tweetNumber
    # queue 2 ALWAYS eventually gets the tweetNumber!
    while runner < tweetNumber:
        # queue 2 'connects' runner in background and main thread
        runner = qu2.get()
        # display progress in ui
        ui.info_message('Loading: {}/{}'.format(runner, tweetNumber), 'blue')
        # ui needs scecific update call
        root.update()
    # queue 3 returns the actual runner from background thread
    # this is necessary because queue 2 ALWAYS retuns the tweet list
    trueAmount = qu3.get()
    # queue 1 transfers the tweetslist
    tweets = qu1.get()
    # close background thread
    background_thread.join()
    print "close background thread"

    # check if there were any tweets retuned
    if not tweets:
        # if the getTweetsByHashtag function did not throw any errors then the hastag does not exist
        if twitter.API_ERROR_CODE == '000':
            ui.info_message("Hashtag does not excist. Please try something else.", 'blue')
            print "Search returned zero tweets."
        # if there are no tweets and getTweetsByHashtag threw an error with code 429 the user has reached the download limit in a previous search
        elif twitter.API_ERROR_CODE == '429':
            ui.info_message("Warning! You have reached the download limit. Please try again in 10 Minutes.")
        # there are no tweets and getTweetsByHashtag threw an untypical error. Something went prober wrong
        else:
            ui.info_message("Error! Something went wrong while trying to load the tweets.")
        # ui needs scecific update call
        root.update()
    # if there are tweets we are good to go
    else:
        # inform the user about the amount of tweets loaded
        ui.info_message("Successfully finished loading! {} tweets were found.".format(trueAmount), 'forest green')
        # if we run into the download limit while downloading the data we still got is in the tweet list and ready to use
        if twitter.API_ERROR_CODE == '429':
            # inform the user that he ran into the download limit and how many tweets we got
            ui.info_message(
                "Warning! You have reached the Download Limit. Loaded {} tweets successfully.".format(trueAmount), 'orange')
        # if some untypical error occured while downloading the errorcode is not 000 and not 429
        elif twitter.API_ERROR_CODE != '000':
            # inform the user that something went wrong and how many tweets we got
            ui.info_message("Warning! Something went wrong. Loaded {} tweets successfully.".format(trueAmount), 'orange')
        # ui needs scecific update call
        root.update()
        # we have tweets to process, lets do it
        process_data(tweets, searchHashtag)


# returns updated HashtagDic using content of one tweet
def get_hashtags(searchStr, dic):
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
def get_country(country, countDic):
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


# Analyze tweets
def process_data(tweets, searchedHash):
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
                HashtagDic = get_hashtags(tweet["text"], HashtagDic)
            if key == "geo":
                # creates a dic 'Countries' : 'countryCount'
                CountryDic = get_country(tweet["geo"], CountryDic)
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
ui.button_auth_ok.bind("<Button-1>", get_auth)
ui.button_auth_tryag.bind("<Button-1>", try_again)
ui.button_search.bind("<Button-1>", validate_input)
# starting screen
ui.display_auth()

# get authentication link
try:
    auth_link, token = twitter.getAuthLink()
except Exception:
    # if we dont get a link there is probably a connection error
    ui.server_connection_error()
else:
    ui.string_auth_link.set(auth_link)

root.mainloop()
