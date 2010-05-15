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
       
    def rollback(self):
        self.con.rollback()