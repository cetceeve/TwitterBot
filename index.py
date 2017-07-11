import api as twitter
import visual

link, token = twitter.getAuthLink()
pin = input(link + ' : ')
if twitter.getToken(pin, token):
    for tweet in twitter.getTweetsByHashtag(q='g20'):
        tweet.text = tweet.text.encode('utf-8').strip()
        print tweet.text
        print ' '

 # visual.barplot()
 # visual.piechart()
 # visual.scatterplot()
