'''
#!C:/Python26/python
import sys
sys.path.append("../classes")
from BeautifulSoup import *
from PeopleInfoCrawler import PeopleInfoCrawler
from PeoplePositionsCrawler import PeoplePositionsCrawler
from AnimeCrawler import AnimeCrawler
from CrawlerFactory import CrawlerFactory
import urllib2, re

print "Content-Type: text/html\n\n"

p = PeoplePositionsCrawler('../data/people.db')

page = 'http://myanimelist.net/people.php?id=3529'
page = 'http://myanimelist.net/people/4/Aya_Hirano'
c=urllib2.urlopen(page)
soup=BeautifulSoup(c.read())

p.addtoindex(page, soup)


'''


import sys
sys.path.append("../classes")
from BeautifulSoup import *
from PeopleInfoCrawler import PeopleInfoCrawler
from PeoplePositionsCrawler import PeoplePositionsCrawler
from AnimeCrawler import AnimeCrawler
from CrawlerFactory import CrawlerFactory


from Database import Database, SqliteDriver
from PeopleInfo import PeopleInfo
p = PeopleInfo(Database(SqliteDriver('../data/people.db')))
p.createindextables()


CrawlerFactory = CrawlerFactory();
CrawlerFactory.registerCrawler(AnimeCrawler('../data/anime.db'))
CrawlerFactory.registerCrawler(PeopleInfoCrawler('../data/people.db'))
CrawlerFactory.registerCrawler(PeoplePositionsCrawler('../data/people.db'))

for i in range(0,10):
    page = "http://myanimelist.net/favorites.php?type=people&limit=%d" % (i * 20)
    CrawlerFactory.crawl([page], 2)
