import api as twitter
import visual

link, token = twitter.getAuthLink()
pin = input(link + ' : ')
if twitter.getToken(pin, token):
    print twitter.getTweetsByHashtag('nog20p')
