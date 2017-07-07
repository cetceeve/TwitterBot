import api as twitter
import visual

link, token = twitter.getAuthLink()
pin = input(link + ' : ')
client = twitter.getToken(pin, token)

print client.me().screen_name
