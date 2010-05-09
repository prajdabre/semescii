#!C:/Python26/python
import cgi
import cgitb; cgitb.enable()

import sys
sys.path.append("classes")
import SearchNet
import AnimeInfo
import Database


search = int(cgi.FieldStorage().getvalue("search"))
titles = [int(k) for k in cgi.FieldStorage().getvalue("titles").split(',')]
selected = int(cgi.FieldStorage().getvalue("selected"))

mynet=SearchNet.SearchNet(
	Database.Database(Database.SqliteDriver('data/nn.db'))
)
#mynet.maketables()
mynet.trainquery([search], titles, selected)


ai = AnimeInfo.AnimeInfo(
	Database.Database(Database.SqliteDriver('data/anime.db'))
)
url = ai.info(selected)[0]

print "Content-Type: text/html\n\n"
print "<script>document.location='%s'</script>" % url