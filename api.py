#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Github: https://github.com/cetceeve/TwitterBot
# Anna Lena Sporrer
# Felix Wieland
from __future__ import print_function
import urlparse
import oauth2 as oauth
import tweepy
import datetime
import json

CONSUMER_KEY        = 'eh9cOj5h3W17QpjSY5X21A0CJ'
CONSUMER_SECRET     = 'neN3X6D8pk54pzo996nGOXeoMLFywi2QTWDe7JEdqzxSB6HDV7'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

# URLs
request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url  = 'https://api.twitter.com/oauth/access_token'
authorize_url     = 'https://api.twitter.com/oauth/authorize'

consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client   = oauth.Client(consumer)


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


def getTweetsByHashtag(q, tweetNumber, geo=True, username=True, timestamp=True):
    query = '%23' + q

    tweet_list = list()
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
            print ('\rLoading: {}/{}'.format(runner, tweetNumber), end='')
    # catch errors
    except Exception as error:
        print ("\nError while loading tweets: ", error)
        raise Exception
    # If everything worked, give back the tweetlist
    else:
        print ("\nDownload successful!")
    finally:
        if not tweet_list:
            raise Exception
        return tweet_list
