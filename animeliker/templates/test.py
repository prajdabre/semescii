#!C:/Python26/python
import cgi
import cgitb; cgitb.enable()
from string import Template
import sys
sys.path.append("classes")
import animeinfo
import pagination
import cPickle
import recommendations

print "Content-Type: text/html\n\n"
print '''
<form action="">
<input type="text" name="q" /> <input type="submit" />
</form>
'''

form = cgi.FieldStorage()
q = form.getvalue("q")


pagination = pagination.pagination('templates/pagination', '/cgi/test.py?q=%s' %q , 100)
pagination.draw()
		
if q != None:
	ai = animeinfo.animeinfo('data/anime.db')
	
	searchid = ai.getId(q)
	recs = ai.getscoredlist(q)[0:100]
	
	ids = []
	for (anime, score) in recs[(pagination.getCurPage() * 10):((pagination.getCurPage() + 1) * 10)]:
		try:
			info = ai.info(anime)
			ids.append(str(anime))
			template = Template( open('templates/anime.phtml', 'r').read() )			
			print template.substitute(
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
		