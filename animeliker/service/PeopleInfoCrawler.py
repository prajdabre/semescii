# -*- coding: utf-8 -*-
from crawler import crawler
from urlparse import urljoin
import urllib2, re
from BeautifulSoup import *
import chardet


class PeopleInfoCrawler(crawler):
    uripattern=ur"^http://myanimelist.net/people.php\?id=[0-9]+$"
    def isindexed(self, page):
        return self.con.execute("select * from people where page='%s'" % page).fetchone()
    
    def addtoindex(self, page, soup):
        if (self.isindexed(page) != None): return False
        
        try:
            name = re.search( '^(.*) - MyAnimeList\.net$', str(soup('title')[0].contents[0]) ).group(1)
        except:
            return False
        
        print "indexing: %s %s" % (page, name)
        
        try:
            member_favorites = str(soup('span', text='Member Favorites:')[0].findParent().findParent().contents[1])
        except:
            return False
        
        try:
            given_name = str(soup('span', text='Given name:')[0].findParent().findParent().contents[1])
            family_name = str(soup('span', text='Family name:')[0].findParent().findParent().contents[7])
        except:
            given_name = None
            family_name = None
        
        try:
            birthday = str(soup('span', text='Birthday:')[0].findParent().findParent().contents[1])
        except: 
            birthday = None
        
        try:
            more = ' '.join( map( str,
                soup('span', text='More:')[0].findParent('td').contents[15:]
            ) )
        except:
            more = None
         
        
        t = ( str(page).decode('utf-8', 'ignore'),
             str(name).decode('utf-8', 'ignore'), 
             str(member_favorites).decode('utf-8', 'ignore'), 
             str(given_name).decode('utf-8', 'ignore'), 
             str(family_name).decode('utf-8', 'ignore'), 
             str(birthday).decode('utf-8', 'ignore'), 
             str(more).decode('utf-8', 'ignore'))
        
        print t
        self.insertrow(t)
        
    
    def insertrow(self, t):
        q = "insert into people(page,name,member_favorites,given_name,family_name,birthday,more) \
             values(?, ?, ?, ?, ?, ?, ?)" 
        self.con.execute(q, t)
        self.dbcommit()    
            
    def createindextables(self):    
        self.con.execute("""
            create table people(page VARCHAR(500),
                                name VARCHAR(500),
                                given_name VARCHAR(500),
                                family_name VARCHAR(500),
                                birthday VARCHAR(500),
                                member_favorites INT,
                                more VARCHAR(5000))                    
        """)
        self.dbcommit()
       