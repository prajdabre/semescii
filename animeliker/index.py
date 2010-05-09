#!C:/Python26/python
import cgi
import cgitb; cgitb.enable()
from string import Template
import sys
import cPickle


sys.path.append("classes")
from Database import Database, SqliteDriver
from AnimeInfo import AnimeInfo
from Pagination import Pagination
import UserRecommendations

print "Content-Type: text/html\n\n"


print Template( open('templates/index.html', 'r').read() ).substitute()
q = cgi.FieldStorage().getvalue("q")

pagination = Pagination('templates/pagination.html', '/cgi/index.py?q=%s' %q , 100)
pagination.draw()	

if q != None:
	ai = AnimeInfo(
		Database(SqliteDriver('data/anime.db'))
	)
	
	searchid = ai.getId(q)
	recs = ai.getscoredlist(q)[0:100]
	
	ids = []
	for (anime, score) in recs[(pagination.getCurPage() * 10):((pagination.getCurPage() + 1) * 10)]:
		try:
			info = ai.info(anime)
			ids.append(str(anime))			
			print Template( open('templates/anime.html', 'r').read() ).substitute(
				title=info[2].split(';|;')[0],
				similarity=score,
				img=info[7], 
				description=info[1], 
				score=info[4], 
				genres=", ".join(info[3].split(';|;')), 
				url="go.py?search=%s&titles=%s&selected=%s" % (searchid, ",".join(ids), anime),
				urldescription = info[0]
			)
		except:
			pass
		