from urlparse import urljoin
import urllib2, re
import chardet

from BeautifulSoup import *
from Crawler import Crawler

class PeopleInfoCrawler(Crawler):
    uripattern=ur"^http://myanimelist.net/people.php\?id=[0-9]+$"
    def isindexed(self, page):
        return self.con.execute("select * from people where page='%s'" % page).fetchone()
    
    def addtoindex(self, page, soup):
        if (self.isindexed(page)): return False
        try:
            name = re.search( '^(.*) - MyAnimeList\.net$', str(soup('title')[0].contents[0]) ).group(1)
            member_favorites = str(soup('span', text='Member Favorites:')[0].findParent().findParent().contents[1])
        except:
            print "Page parsing error."
            return False
        
        print "People Info Crawler. Indexing: %s (%s)" % (page, name)
        
        try:
            given_name = str(soup('span', text='Given name:')[0].findParent().findParent().contents[1])
            family_name = str(soup('span', text='Family name:')[0].findParent().findParent().contents[7])
        except:
            given_name = ''
            family_name = ''
        
        try:
            birthday = str(soup('span', text='Birthday:')[0].findParent().findParent().contents[1])
        except: 
            birthday = ''
        
        try:
            more = ' '.join( map( str,
                soup('span', text='More:')[0].findParent('td').contents[15:]
            ) )
        except:
            more = ''
         
        
        self.insertrow(
            (str(page).decode('utf-8', 'ignore'),
             str(name).decode('utf-8', 'ignore'), 
             str(member_favorites).decode('utf-8', 'ignore'), 
             str(given_name).decode('utf-8', 'ignore'), 
             str(family_name).decode('utf-8', 'ignore'), 
             str(birthday).decode('utf-8', 'ignore'), 
             str(more).decode('utf-8', 'ignore'))
        )
        
    
    def insertrow(self, t):
        q = "insert into people(page,name,member_favorites,given_name,family_name,birthday,more) \
             values(?, ?, ?, ?, ?, ?, ?)" 
        self.con.execute(q, t)
        self.con.commit()
          
       