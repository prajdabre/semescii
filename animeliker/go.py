#!C:/Python26/python
import cgi
import cgitb; cgitb.enable()

import sys
sys.path.append("classes")
import nn
import animeinfo
import database



search = int(cgi.FieldStorage().getvalue("search"))
titles = [int(k) for k in cgi.FieldStorage().getvalue("titles").split(',')]
selected = int(cgi.FieldStorage().getvalue("selected"))

mynet=nn.searchnet(
	database.Database(database.SqliteDriver('data/nn.db'))
)
#mynet.maketables()
mynet.trainquery([search], titles, selected)


ai = animeinfo.animeinfo(
	database.Database(database.SqliteDriver('data/anime.db'))
)
url = ai.info(selected)[0]

print "Content-Type: text/html\n\n"
print "<script>document.location='%s'</script>" % url




