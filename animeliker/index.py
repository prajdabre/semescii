#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.stderr = sys.stdout
import cgi

print "Content-Type: text/html\n\n"
sys.path.append('/var/www')
from jinja2 import Template
from django.utils.encoding import smart_str, smart_unicode

from testing.timeit import timeit
from database.Database import Database
from database.SqliteDriver import SqliteDriver
from anisearch.AnimeInfo import AnimeInfo

@timeit
def index(**kwargs):
    if kwargs['q'] is None: q = ''
    else: q = str(kwargs['q'])
    
    try: page = int(kwargs['page'])
    except: page = 0

    AnimeList = None
    if q:
        AnimeList = getAnimeList(q, page)

    template = Template(open('/var/www/templates/index.html', 'r').read())
    print template.render(q=q, page=page, AnimeList=AnimeList)


@timeit
def getAnimeList(q, page=0, rows_per_page=10):    
    anisearch = AnimeInfo(Database(SqliteDriver('/var/www/data/anime.db')))
    searchid = anisearch.getId(q)
    if searchid == None:
        return None
    recs = anisearch.getscoredlist(searchid)[page*rows_per_page : page*rows_per_page+rows_per_page]
            
    AnimeList = []            
    ids = []
    for (id, similarity) in recs:
            info = anisearch.info(id)
            if info is None: continue
            
            ids.append(str(id))      
            info['similarity'] = similarity
            info['url'] = "go.py?search=%s&titles=%s&selected=%s" % (searchid, ",".join(ids), id)
            AnimeList.append(info) 

    return AnimeList
 


index(q=cgi.FieldStorage().getvalue('q'), 
      page=cgi.FieldStorage().getvalue('page'))   

