from BeautifulSoup import *
from PeopleInfoCrawler import PeopleInfoCrawler
from PeoplePositionsCrawler import PeoplePositionsCrawler
from AnimeCrawler import AnimeCrawler
import urllib2, re
from urlparse import urljoin

class CrawlerFactory():
    crawlers = []
    
    def registerCrawler(self, crawler):
        self.crawlers.append(crawler)
            
    def crawl(self,pages,depth=2, pattern=None):
        for i in range(depth):
            newpages=set()
            for page in pages:
                try:
                    c=urllib2.urlopen(page)
                except:
                    print "Network connection troubles. Can't connect with: %s" % page
                    continue
                
                soup=BeautifulSoup(c.read())
                for crawler in self.crawlers:
                    if re.search(crawler.uripattern, page) != None:
                        crawler.addtoindex(page, soup)  
                links=soup('a')
                for link  in links:
                    if('href' in dict(link.attrs)):
                        url=urljoin(page, link['href'])
                        if url.find("'")!=-1: continue
                        url=url.split('#')[0]
                         
                        if url[0:4] != 'http': 
                            continue 
                        for crawler in self.crawlers:
                            if (re.search(crawler.uripattern, url) != None and
                                crawler.isindexed(url) == False):
                                newpages.add(url)
                                                                                          
                pages=newpages
 

    
CrawlerFactory = CrawlerFactory();
CrawlerFactory.registerCrawler(AnimeCrawler('../data/anime.db'))
CrawlerFactory.registerCrawler(PeopleInfoCrawler('../data/people.db'))
CrawlerFactory.registerCrawler(PeoplePositionsCrawler('../data/people_positions.db'))


for i in range(600, 620):
    page = "http://myanimelist.net/favorites.php?type=people&limit=%d" % (i * 20)
    CrawlerFactory.crawl([page], 10)
