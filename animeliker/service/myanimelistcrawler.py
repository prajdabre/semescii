# -*- coding: utf-8 -*-
import crawler
    
class myanimelistcrawler(crawler):     
        
    def isindexed(self, page):
        return self.con.execute("select * from anime where page='%s'" % page).fetchone()
    
    def isuptodate(self, page):
        self.con.execute("select * from anime where page='%s' and")
        return False        
        
    def addtoindex(self, page, soup):
        if (self.isindexed(page) != None): return
        print "indexing: %s" % page 

        try:
            score = float(soup('span', text='Score:')[0].findParent().findParent().contents[1])
        except:
            return
        
        try:
            description = ''.join([ str(k) for k in 
                                    soup('h2', text='Synopsis')[1].findParent().findParent().contents[1:] ])
        except:
            description = None
        
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
            genres = ";|;".join(genres)
        except:
            genres = ''
        
        
        try:
            tags = [ re.search( '([0-9]+) people tagged with (.*)$', str(k['title']) ).group(1, 2) for k in
                            soup.findAll('a', title=re.compile('[0-9]+ people tagged with')) ]
            tags = ";|;".join( [ ":".join(k) for k in tags ] )
        except:
            tags = ''

            
        try:
            producers = [ str(k.contents[0]) for k in
                                soup.findAll('a', href=re.compile("http:\/\/myanimelist\.net\/anime\.php\?p=[0-9]+")) ]
            producers = ";|;".join(producers)
        except:    
            producers = ''
            
        try:
            img = soup.find('img', href=re.compile('^http\:\/\/cdn.myanimelist.net\/images\/anime\/.*'))['src']
        except:
            img = ''

            
        t = ( str(page).decode('utf-8', 'ignore'),
             str(description).decode('utf-8', 'ignore'), 
             str(titles).decode('utf-8', 'ignore'), 
             str(genres).decode('utf-8', 'ignore'), 
             str(score).decode('utf-8', 'ignore'), 
             str(tags).decode('utf-8', 'ignore'), 
             str(producers).decode('utf-8', 'ignore'),
             str(img).decode('utf-8', 'ignore'))
        self.insertrow(t)
    
    
    def insertrow(self, t):
        q = "insert into anime(page, description,titles,genres,score,tags,producers,img) \
             values(?, ?, ?, ?, ?, ?, ?, ?)" 
        self.con.execute(q, t)
        self.dbcommit()  
        
    def updaterow(self, t):
        pass   
            
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

    
crawler = myanimelistcrawler('../data/anime.db')

for i in range(108, 900):
    page = "http://myanimelist.net/topanime.php?type=&limit=%d" % (i * 30)
    crawler.crawl([page], 10, pattern=ur"^http://myanimelist.net/anime/[0-9]+/[^\/]*$")

    
#page = "http://myanimelist.net/anime/202/Wolfs_Rain"
#crawler.crawl([page], 10, pattern=ur"^http://myanimelist.net/anime/[0-9]+/[^\/]*$")