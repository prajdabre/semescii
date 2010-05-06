from Crawler import Crawler
import re

class PeoplePositionsCrawler(Crawler):
    uripattern=ur"^http://myanimelist.net/people.php\?id=[0-9]+$"
    def isindexed(self, page):
        return False
    
    def addtoindex(self, page, soup):
        print "indexed"
        people_id = re.search( '^(.*) - MyAnimeList\.net$', str(soup('title')[0].contents[0]) ).group(1)
        contents = soup.findAll(text='Anime Staff Positions')[0].findNext('table').findAll('tr')
        for tr in contents:        
        	try:
        	    position = tr.findAll('small')[0].contents[0]
        	    anime_id = tr.findAll('a')[1].contents[0]
        	except:
        		continue
        	
        	print "%s:%s" % (position, anime_id)
        
            
    def insertrow(self, t):
        q = "insert into anime_positions(position, anime_id, people_id) \
             values(?, ?, ?)" 
        self.con.execute(q, t)
        self.dbcommit()    
        
    
    def createindextables(self):
        self.con.execute("""
            create table anime_positions(position VARCHAR(500)
                                         anime_id INT,
                                         people_id INT)
        """)
        self.dbcommit()
