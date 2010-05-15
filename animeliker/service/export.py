# -*- coding: utf-8 -*-
from pysqlite2 import dbapi2 as sqlite
import pickle
import sys


try:
  dbname = sys.argv[1]
  save_to_file = sys.argv[2]
except IndexError:
  print "Enter sqlite database name and file to export."
  print "Example:"
  print "export.py database.db filetosave.txt"
  exit()
 

con = sqlite.connect(dbname)
tables_info = con.execute("SELECT * FROM sqlite_master").fetchall()
result = {}
for table_info in tables_info:
  tablename = table_info[1]
  data = con.execute("SELECT *, rowid FROM `%s`" %tablename).fetchall();
  result[tablename] = data

pickle.dump(result, open(save_to_file, 'w'))


