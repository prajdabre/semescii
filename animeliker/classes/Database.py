from pysqlite2 import dbapi2 as sqlite

#sqlite database driver
class SqliteDriver:
    def __init__(self, dbname):
        self.con=sqlite.connect(dbname)
    def query(self, query):
        pass
    def execute(self, query, params=False):
        if (params != False):
            return self.con.execute(query, params)
        return self.con.execute(query);
    def __del__(self):
        self.con.close()
        
    def commit(self):
        self.con.commit()
       

#Google App Engine database driver
class AppEngineDriver:
    def __init__(self, dbname):
        pass
    def query(self, query):
        pass
    def execute(self, query):
        pass
    def __del__(self):
        pass    

class Resource:
    def __init__(self, data):
        pass
    
    def fetchall(self):
        return self.data
    
    def fetchone(self):
        return pop(self.data)
    
    

class Database:
    def __init__(self, driver):
        self.driver = driver
    def query(self, query):
        self.driver.query(query)
        
    def execute(self, query, params=False):
        return self.driver.execute(query, params)
    
    def commit(self):
        self.driver.commit()