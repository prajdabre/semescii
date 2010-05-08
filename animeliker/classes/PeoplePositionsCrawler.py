from Crawler import Crawler
from Database import Database, SqliteDriver
from AnimeInfo import AnimeInfo
from AnimeCrawler import AnimeCrawler
from PeopleInfo import PeopleInfo
import re

class PeoplePositionsCrawler(Crawler):
    uripattern=ur"^http://myanimelist.net/people.php\?id=[0-9]+$"
    def isindexed(self, page):
        return (self.con.execute("""
        		select * from anime_positions, anime_acting_roles 
        		where anime_positions.people_id = (select rowid from people where page='%s')
        		or anime_acting_roles.people_id = (select rowid from people where page='%s')
				""" % (page, page))).fetchall()
    
    def getAnimeId(self, tr):
        ai = AnimeInfo(Database(SqliteDriver('../data/anime.db')))
        id = ai.getId(tr.findAll('a')[1].contents[0])
        if not id:
            anime_link = tr.findAll('a')[1]['href']
            animecrawler = AnimeCrawler('../data/anime.db')
            animecrawler.crawl([anime_link], 1)
            id = ai.getId(tr.findAll('a')[1].contents[0])
        return id
    
    def addtoindex(self, page, soup):
        print "People Positions Crawler. Indexing %s: " % page
        
        peopleinfo = PeopleInfo(Database(SqliteDriver('../data/people.db')))
        people_id = peopleinfo.getId(
    		re.search( '^(.*) - MyAnimeList\.net$', str(soup('title')[0].contents[0]) ).group(1)
    	)              
        
        
        
        #parsing Acting Roles
        contents = soup.findAll(text='Voice Acting Roles')[0].findNext().contents
        for tr in contents:
            if len(str(tr)) < 40: continue
            anime_id = self.getAnimeId(tr)
            character_name = tr.findAll('a')[3].contents[0]
            character_type = tr.findAll('div', {'class':'spaceit_pad'})[1].contents[0].string.replace("&nbsp;","")
            
            self.insertActingRole(
                (str(people_id).decode('utf-8', 'ignore'),
                str(anime_id).decode('utf-8', 'ignore'),
                str(character_name).decode('utf-8', 'ignore'),
                str(character_type).decode('utf-8', 'ignore'))
            )
            
        #parsing Staff Positions
        contents = soup.findAll(text='Anime Staff Positions')[0].findNext().contents
        for tr in contents:        
            if len(str(tr)) < 40: continue
            anime_id = self.getAnimeId(tr)
            position = tr.findAll('small')[0].contents[0]
                       	
            self.insertStaffPosition(
                (str(position).decode('utf-8', 'ignore'),
                str(anime_id).decode('utf-8', 'ignore'), 
                str(people_id).decode('utf-8', 'ignore'))
            )
        self.con.commit()    
        
        	
    def insertActingRole(self, t):
    	q = "insert into anime_acting_roles(people_id, anime_id, character_name, character_type) \
             values(?, ?, ?, ?)" 
        self.con.execute(q, t)
        
        		        
    def insertStaffPosition(self, t):
        q = "insert into anime_positions(position, anime_id, people_id) \
             values(?, ?, ?)" 
        self.con.execute(q, t)
            
        
