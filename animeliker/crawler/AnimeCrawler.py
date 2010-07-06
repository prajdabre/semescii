import re

from Crawler import Crawler
    
class AnimeCrawler(Crawler):     
    uripattern=ur"^http://myanimelist.net/anime/[0-9]+/[^\/]+$"
    def isindexed(self, page):
        return (self.con.execute("select * from anime where page='%s'" % page).fetchone() != None)
    
    def isuptodate(self, page):
        self.con.execute("select * from anime where page='%s' and")
        return False        
        
    def addtoindex(self, page, soup):
        if (self.isindexed(page)): return
        print "Anime Crawler. Indexing: %s" % page
        try:
            score = float(soup('span', text='Score:')[0].findParent().findParent().contents[1])
        except:
            return False
        
        try:
            description = ''.join([ str(k) for k in 
                                    soup('h2', text='Synopsis')[1].findParent().findParent().contents[1:] ])
        except:
            description = ''
        
        maintitle = re.search( '^(.*) - MyAnimeList\.net$', str(soup('title')[0].contents[0]) ).group(1)
        try:
            engtitle = str(soup('span', text='English:')[0].findParent().findParent().contents[1])
        except: 
            engtitle = ''
        try:
            jptitle = str(soup('span', text='Japanese:')[0].findParent().findParent().contents[1])
        except:
            jptitle = ''
        titles = [maintitle, engtitle, jptitle]
        titles = ";|;".join(titles)
        
        try:
            genres = [ str(self.gettextonly(k)) for k in 
                            soup('span', text='Genres:')[0].findParent().findParent().contents[2:] if k != ', ' ]
        except:
            genres = []
        
        
        try:
            tags = [ re.search( '([0-9]+) people tagged with (.*)$', str(k['title']) ).group(1, 2) for k in
                            soup.findAll('a', title=re.compile('[0-9]+ people tagged with')) ]
        except:
            tags = []

            
        try:
            producers = [ str(k.contents[0]) for k in
                                soup.findAll('a', href=re.compile("http:\/\/myanimelist\.net\/anime\.php\?p=[0-9]+")) ]
        except:    
            producers = []
        try:
            img = soup.find('img', src=re.compile('^http\:\/\/cdn.myanimelist.net\/images\/anime\/.*'))['src']
        except:
            img = 'http://cdn.myanimelist.net/images/na_series.gif'
        anime_id = self.con.execute("SELECT max(rowid) FROM anime").fetchone()[0] + 1

        for (count, tag_name) in tags:
            q = "INSERT INTO tags(anime_id, tag_name, count) VALUES(?, ?, ?)"
            t = ( anime_id,
                  str(tag_name).decode('utf-8', 'ignore'),
                  count )
            self.con.execute(q, t)

        for producer in producers:
            q = "INSERT INTO producers(anime_id, producer_name) VALUES(?, ?)"
            t = ( anime_id,
                  str(producer).decode('utf-8', 'ignore') )
            self.con.execute(q, t)  
        
        for genre in genres:
            q = "INSERT INTO genres(anime_id, genre_name) VALUES(?, ?)"
            t = ( anime_id,
                  str(genre).decode('utf-8', 'ignore') )
            self.con.execute(q, t)    
         
        t = (anime_id,  
             str(page).decode('utf-8', 'ignore'),
             str(description).decode('utf-8', 'ignore'), 
             str(titles).decode('utf-8', 'ignore'), 
             str(score).decode('utf-8', 'ignore'), 
             str(img).decode('utf-8', 'ignore'))
        q = "insert into anime(rowid, page, description, titles, score, img) \
             values(?, ?, ?, ?, ?, ?)" 
        self.con.execute(q, t)
        
        
        self.con.commit()
        
        
    def updaterow(self, t):
        q = """
            update anime set
            page = ?,
            description = ?,
            titles = ?,
            genres = ?,
            score = ?,
            tags = ?,
            producers =?,
            img = ?
            where rowid = ?
        """
        self.con.execute(q, t)
        self.dbcommit()
            
    def createindextables(self):
        self.con.execute("""
            create table anime(page VARCHAR(500), 
                               description TEXT,
                               titles VARCHAR(500),
                               genres VARCHAR(500),
                               score FLOAT,
                               tags VARCHAR(500),
                               producers VARCHAR(500),
                               img VARCHAR(500))
        """)
        self.dbcommit()
