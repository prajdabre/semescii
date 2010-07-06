import urllib2, re
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup
import chardet


class CrawlerFactory():
    crawlers = []
    
    def registerCrawler(self, crawler):
        self.crawlers.append(crawler)
            
    def crawl(self,pages,depth=2, pattern=None):
        for i in range(depth):
            newpages=set()
            for page in pages:
                try:
                    print "Opening: %s" % page
                    contents=urllib2.urlopen(page).read()                    
                except:
                    print "Network connection troubles. Can't connect with: %s" % page
                    continue
                
                contents = contents.replace("</scr'+'ipt>", '')
                
                soup=BeautifulSoup(contents)              
                for crawler in self.crawlers:
                    if (re.search(crawler.uripattern, page)
                       and not crawler.isindexed(page)):
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
                            if (re.search(crawler.uripattern, url) 
                                and not crawler.isindexed(url)):
                                newpages.add(url)
                                                                                   
                pages=newpages           