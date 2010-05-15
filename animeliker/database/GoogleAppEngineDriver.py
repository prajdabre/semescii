from google.appengine.ext import db

#Google App Engine database driver
class AppEngineDriver:
    def __init__(self):
        pass
    def query(self, query):
        pass
    def execute(self, query, params=False):
        return Resource(db.GqlQuery(query))
    def __del__(self):
        pass    

class Resource:
    def __init__(self, data):
        self.data = data
            
    def fetchall(self):
        return self.data.fetch(10000)
    
    def fetchone(self):
        try:
            return self.data.fetch(1)[0]
        except IndexError:
            return None