# import requests
import urlparse
import oauth2 as oauth
import tweepy

# TODO: Remove these values and ask for user values
CONSUMER_KEY        = 'eh9cOj5h3W17QpjSY5X21A0CJ'
CONSUMER_SECRET     = 'neN3X6D8pk54pzo996nGOXeoMLFywi2QTWDe7JEdqzxSB6HDV7'

# URLs
request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url  = 'https://api.twitter.com/oauth/access_token'
authorize_url     = 'https://api.twitter.com/oauth/authorize'

consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client   = oauth.Client(consumer)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

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

    auth.set_access_token(access_token['oauth_token'], access_token['oauth_token_secret'])

    return (access_token['oauth_token'], access_token['oauth_token_secret'])
