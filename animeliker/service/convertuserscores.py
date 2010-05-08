import sys
sys.path.append("../classes")


import cPickle
import urllib2, re
from BeautifulSoup import *
from django.utils.encoding import smart_str, smart_unicode

#array flip converter

'''
file = "data/usersAnimeScores.txt"	
usersAnimeScores = cPickle.load( open(file, 'r') )


from pysqlite2 import dbapi2 as sqlite

import animeinfo
converted = {}
ai = animeinfo.animeinfo('data/anime.db')
len = len(usersAnimeScores)
i = 0
for user in usersAnimeScores:
	list2 = {}
	for anime in usersAnimeScores[user]:
		id = ai.getId(anime)
		list2[id] = usersAnimeScores[user][anime]
		
	converted[user] = list2
	i += 1
	print '%d from %d' % (i, len)
	
cPickle.dump(converted, open('userscores.txt', 'w'))
'''

import UserRecommendations
p = cPickle.load( open("../data/userscores.txt", 'r') )
r = UserRecommendations.transformPrefs(p)
cPickle.dump(r, open('../data/userscoresfliped.txt', 'w'))
