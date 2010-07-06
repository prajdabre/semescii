from Crawler import Crawler
from AnimeCrawler import AnimeCrawler

from database.Database import Database
from database.SqliteDriver import SqliteDriver 
from anisearch.AnimeInfo import AnimeInfo
from anisearch.PeopleInfo import PeopleInfo
import re

class PeoplePositionsCrawler(Crawler):
    uripattern=ur"^http://myanimelist.net/people.php\?id=[0-9]+$"
    def isindexed(self, page):
        count1 = (self.con.execute("""
        		select count(anime_id) from anime_positions
        		where anime_positions.people_id = (select rowid from people where page='%s')
				""" % (page))).fetchone()[0]
        count2 = (self.con.execute("""
                select count(anime_id) from anime_acting_roles
                where anime_acting_roles.people_id = (select rowid from people where page='%s')
                """ % (page))).fetchone()[0]             
        return ((count1 > 0) or (count2 > 0))
    
    def getAnimeId(self, tr):
        ai = AnimeInfo(self.con)
        id = ai.getId(tr.findAll('a')[1].contents[0])
        if not id:
            anime_link = tr.findAll('a')[1]['href']
            animecrawler = AnimeCrawler(self.con)
            animecrawler.crawl([anime_link], 1)
            id = ai.getId(tr.findAll('a')[1].contents[0])
        return id
    
    def addtoindex(self, page, soup):
        if (self.isindexed(page)): return
        print "People Positions Crawler. Indexing %s: " % page
        
        peopleinfo = PeopleInfo(self.con)
        people_id = peopleinfo.getIdByPage(page)              
        
        
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
            
        
