class PeopleInfo:
    def __init__(self, con):
        self.con = con
	
    def getId(self, name):
        return self.con.execute('select rowid from people where name = ?', (name,)).fetchone()[0]
	
    def createindextables(self):
        self.con.execute("""
            create table if not exists `anime_positions`
            	(position VARCHAR(500),
                anime_id INT,
                people_id INT)
        """)
		
        self.con.execute("""
			create table if not exists `anime_acting_roles`
				(people_id INT,
				anime_id INT,
				character_name VARCHAR(500),
				character_type VARCHAR(50))
		""")
		
        self.con.execute("""
            create table if not exists `people`
            	(page VARCHAR(500),
                name VARCHAR(500),
                given_name VARCHAR(500),
                family_name VARCHAR(500),
                birthday VARCHAR(500),
                member_favorites INT,
                more VARCHAR(5000))                    
        """)
        