import api as twitter
import visual

link, token = twitter.getAuthLink()
pin = input(link + ' : ')
if twitter.getToken(pin, token):
    print 'Your name is: ' + twitter.api.me().screen_name
