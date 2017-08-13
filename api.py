#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Github: https://github.com/cetceeve/TwitterBot
# Anna Lena Sporrer
# Felix Wieland
# Fabian Zeiher
from __future__ import print_function
import urlparse
import oauth2 as oauth
import tweepy
import datetime
import json

API_ERROR_CODE = '000'

CONSUMER_KEY = 'eh9cOj5h3W17QpjSY5X21A0CJ'
CONSUMER_SECRET = 'neN3X6D8pk54pzo996nGOXeoMLFywi2QTWDe7JEdqzxSB6HDV7'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

# URLs
request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'

consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client = oauth.Client(consumer)


# request_token und access_token Methode von https://github.com/joestump/python-oauth2/wiki/Twitter-Three-legged-OAuth
def getAuthLink():
    resp, content = client.request(request_token_url, 'GET')
    if resp['status'] != '200':
        raise Exception('Invalid response %s.' % resp['status'])

    request_token = dict(urlparse.parse_qsl(content))

    return ('%s?oauth_token=%s' % (authorize_url, request_token['oauth_token']), request_token)


def getToken(pin, request_token):
    token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(pin)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, 'POST')
    access_token = dict(urlparse.parse_qsl(content))
    try:
        auth.set_access_token(access_token['oauth_token'], access_token['oauth_token_secret'])
        return True
    except Exception, e:
        return False


def getTweetsByHashtag(q, tweetNumber, qu1, qu2, qu3, geo=True, username=True, timestamp=True):
    # API_ERROR_CODE needs to be a global variable because it is used in index.py
    global API_ERROR_CODE
    # construct the query
    query = '%23' + q
    # initialize the tweet_list
    tweet_list = list()
    # track the amount of returned tweets
    runner = 0
    # try loading the tweets
    try:
        # cursor reads through tweets until set tweetNumber is reached, saves one tweet into a status Object
        # from which the desired information is extracted and saved into a dictionary
        # every tweet Dicionary is then added to the complete tweet_list
        for status in tweepy.Cursor(api.search, q=query, rpp=100).items(tweetNumber):
            tweet = {}
            tweet["text"] = status.text
            tweet["username"] = status.user.name
            tweet["geo"] = status.user.lang
            # not always are coordinates available -> set coord to '0'
            coord = status.coordinates
            if coord is not None:
                coord = str(status.coordinates.get("coordinates"))
                tweet["coordinates"] = coord
            else:
                coord = "0"
                tweet["coordinates"] = coord
            # convert timestamp into usable string
            tweet["timestamp"] = str(status.created_at.strftime('%a %b %d %H:%M:%S'))
            tweet_list.append(tweet)
            runner += 1
            # give new runner value to the queue
            qu2.put(runner)
            print ('\rLoading: {}/{}'.format(runner, tweetNumber), end='')
    # catch errors
    except Exception as error:
        # the error message always contains the html error code at the end
        API_ERROR_CODE = str(error)[-3:]
        print (' >> Exception while loading tweets:', error)
    else:
        # If everything worked make sure the error code is neutral
        API_ERROR_CODE = '000'
        print (" >> Download successful!")
    # always give something to the queues in order to close the background thread
    finally:
        # the runner resembles the true amount of loaded tweets, it now goes into queue 3
        qu3.put(runner)
        # this closes a while loop in the main thread
        # this is ABSOLUTLY NECESSARY to close the background thread
        qu2.put(tweetNumber)
        # we need the tweet list back, no matter how many tweets are in it
        qu1.put(tweet_list)
