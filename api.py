# import requests
import urlparse
import oauth2 as oauth

# TODO: Remove these values and ask for user values
CONSUMER_KEY        = 'eh9cOj5h3W17QpjSY5X21A0CJ'
CONSUMER_SECRET     = 'neN3X6D8pk54pzo996nGOXeoMLFywi2QTWDe7JEdqzxSB6HDV7'
ACCESS_TOKEN        = '1531973461-rjDvE9sPxodCSQsaVcZry09h4kTQ8JVOzsyxdx0'
ACCESS_TOKEN_SECRET = 'kFaJzviuCsXAwAWZDePntMzphXcJAgLNgRDraiNM603CM'

# URLs
request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url  = 'https://api.twitter.com/oauth/access_token'
authorize_url     = 'https://api.twitter.com/oauth/authorize'

consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client   = oauth.Client(consumer)

# Get request token
resp, content = client.request(request_token_url, 'GET')
if resp['status'] != '200':
    raise Exception('Invalid response %s.' % resp['status'])

request_token = dict(urlparse.parse_qsl(content))

# Output link to authorization
print '%s?oauth_token=%s' % (authorize_url, request_token['oauth_token'])

# wait for auth
acc = 'n'
while acc.lower() == 'n':
    acc = raw_input('Have you authorized me? (y/n) ')
oauth_verifier = raw_input('PIN')

# Get and use token
token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

resp, content = client.request(access_token_url, 'POST')
access_token = dict(urlparse.parse_qsl(content))

print '%s and %s' % (access_token['oauth_token'], access_token['oauth_token_secret'])
