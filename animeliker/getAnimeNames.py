#!C:/Python26/python
print "Content-Type: text/html\n\n"
import json
import cgi
import sys
sys.path.append("classes")
import Database


q = cgi.FieldStorage().getvalue("q")
try:
	con = Database.Database(Database.SqliteDriver('data/anime.db'))
	results = []
	res=con.execute('''
	   select rowid, titles from anime where titles like ? limit 15
	''', ('%' + q + '%',)).fetchall()
	for row in res:
		results.append({
		    "value": (row[1].split(';|;')[0]), 
			"info": ("%s, %s" % (row[1].split(';|;')[1], row[1].split(';|;')[2]) )
		})
	print json.dumps({"results": results})
except TypeError:
	print "IO Error"