class Database:
    def __init__(self, driver):
        self.driver = driver
        
    def execute(self, query, params=False):
        return self.driver.execute(query, params)
    
    def commit(self):
        self.driver.commit()
        
    def rollback(self):
        self.driver.rollback()