import sys
sys.path.append('/var/www')

from anisearch.SearchNet import SearchNet
from anisearch.AnimeInfo import AnimeInfo
from database.Database import Database
from database.SqliteDriver import SqliteDriver

def index(req, **kwargs):
    req.content_type = "text/html"
    req.send_http_header()
    
    search = int(kwargs["search"])
    titles = [int(k) for k in kwargs["titles"].split(',')]
    selected = int(kwargs["selected"])
    
    mynet=SearchNet(
        Database( SqliteDriver('/var/www/data/nn.db'))
    )
    #mynet.maketables()
    mynet.trainquery([search], titles, selected)
	
	

    anisearch = AnimeInfo(
        Database(SqliteDriver('/var/www/data/anime.db'))
    )
    url = anisearch.info(selected)[0]
    
    return "<script>document.location='%s'</script>" % url