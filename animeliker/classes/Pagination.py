import cgi
import cgitb; cgitb.enable()
class Pagination:
	def __init__(self, templatefile, url, len, rowsperpage = 10):
		self.templatefile = templatefile
		self.len = len
		self.url = url
		self.rowsperpage = rowsperpage
	
	def draw(self):
		for i in range(1, (self.len / self.rowsperpage) + 1):
			print '''
				<a href="%s&page=%d">%d</a>
			''' % (self.url, i, i)
		
	def getCurPage(self):
		try:
			return int(cgi.FieldStorage().getvalue('page')) - 1
		except:
			return 0