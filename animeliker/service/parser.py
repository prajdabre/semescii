import sys
sys.path.append("../classes")
from BeautifulSoup import *
from PeopleInfoCrawler import PeopleInfoCrawler
from PeoplePositionsCrawler import PeoplePositionsCrawler
from AnimeCrawler import AnimeCrawler
from CrawlerFactory import CrawlerFactory



    
CrawlerFactory = CrawlerFactory();
CrawlerFactory.registerCrawler(AnimeCrawler('../data/anime.db'))
CrawlerFactory.registerCrawler(PeopleInfoCrawler('../data/people.db'))
CrawlerFactory.registerCrawler(PeoplePositionsCrawler('../data/people_positions.db'))


for i in range(100,120):
    page = "http://myanimelist.net/favorites.php?type=people&limit=%d" % (i * 20)
    CrawlerFactory.crawl([page], 10)

