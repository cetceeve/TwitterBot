import twitter
import tkinter

CONSUMER_KEY = 'eh9cOj5h3W17QpjSY5X21A0CJ'
CONSUMER_SECRET = 'neN3X6D8pk54pzo996nGOXeoMLFywi2QTWDe7JEdqzxSB6HDV7'
ACCESS_TOKEN = '1531973461-rjDvE9sPxodCSQsaVcZry09h4kTQ8JVOzsyxdx0'
ACCESS_TOKEN_SECRET = 'kFaJzviuCsXAwAWZDePntMzphXcJAgLNgRDraiNM603CM'

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)

search = api.GetSearch(raw_query='q=%23cofveve', count=1)

print [p.text for p in search]
