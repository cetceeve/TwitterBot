import api as twitter
import visual

#API
link, token = twitter.getAuthLink()
pin = input(link + ' : ')
if twitter.getToken(pin, token):
    print twitter.getTweetsByHashtag('nog20p')

#Visualisierung
vis = visual.Visual()
vis.barplot()
vis.piechart()
vis.scatterplot()
vis.globalscatter()
vis.display()