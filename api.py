# import requests
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


def getTweetsByHashtag(q, geo=True, username=True, timestamp=True):
    if q is None:
        raise Exception("Query string can't be None")
    query = '%23' + q

    results = list()
    for status in tweepy.Cursor(api.search, q=query, rpp=100).items(1000):
        results.append(status)
    # results = api.search(q=query, rpp=100)

    tweet_list = list()
    for t in results:
        tweet = {}
        tweet["text"] = t.text
        tweet["username"] = t.user.name
        tweet["geo"] = t.user.lang

        coord = t.coordinates
        if coord is not None:
            coord = str(t.coordinates.get("coordinates"))
            tweet["coordinates"] = coord
        else:
            coord = "0"
            tweet["coordinates"] = coord

        tweet["timestamp"] = str(t.created_at.strftime('%a %b %d %H:%M:%S'))
        tweet_list.append(tweet)

    return tweet_list
