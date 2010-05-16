from database.Database import Database
from database.SqliteDriver import SqliteDriver

con = Database(SqliteDriver('../../data/anime.db'))

res = con.execute("SELECT rowid, tags FROM anime").fetchall()
for row in res:
    rowid = row[0]
    tags = row[1].split(';|;')
    
    for tag in tags:
        if tag == '': continue
        print tag
        (count, tag_name) = tag.split(':')

        con.execute("""
            INSERT INTO tags
            (anime_id, tag_name, count) VALUES
            (?, ?, ?)
            """, (rowid, tag_name, count))


con.commit()

