from pysqlite2 import dbapi2 as sqlite

import nn	

class searcher:
	def __init__(self,dbname):
		self.con=sqlite.connect(dbname)
		
	def __del__(self):
		self.con.close()
	
	def getmatchrows(self,q):
		fieldlist='w0.urlid'
		tablelist=''
		clauselist=''
		wordids=[]
		
		words=q.split(' ')
		tablenumber=0
		
		for word in words:
			wordrow=self.con.execute(
				"select rowid from wordlist where word='%s'" % word).fetchone( )
			if wordrow!=None:
				wordid=wordrow[0]
				wordids.append(wordid)
				if tablenumber>0:
					tablelist+=','
					clauselist+=' and '
					clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1,tablenumber)
				fieldlist+=',w%d.location' % tablenumber
				tablelist+='wordlocation w%d' % tablenumber
				clauselist+='w%d.wordid=%d' % (tablenumber, wordid)
				tablenumber+=1
			
			fullquery='select %s from %s where %s' % (fieldlist, tablelist, clauselist)
			cur=self.con.execute(fullquery)
			rows=[row for row in cur]
			
			return rows,wordids
			
	def getscoredlist(self,rows,wordids,q):
		totalscores=dict([(row[0],0) for row in rows])
		
		#scoring
		weights=[(1.0, self.frequencyscore(rows)),
				 (1.0, self.locationscore(rows)),
				 (1.0, self.distancescore(rows)),
				 (1.0, self.inboundlinkscore(rows)),
				 (1.0, self.nnscore(rows,wordids))]
		
		for (weight, scores) in weights:
			for url in totalscores:
				totalscores[url]+=weight*scores[url]
		return totalscores
		
	def geturlname(self,id):
		return self.con.execute(
		"select url from urllist where rowid=%d" %id).fetchone()[0]
		
	def query(self,q):
		rows,wordids = self.getmatchrows(q)
		scores=self.getscoredlist(rows,wordids,q)
		rankedscores=sorted([(score,url) for (url,score) in scores.items()],\
		reverse=1)
		return rankedscores
			
	def normalizescores(self,scores,smallIsBetter=0):
		vsmall=0.00001
		if smallIsBetter:
			minscore=min(scores.values())
			return dict([ (u,float(minscore)/max(vsmall,l)) for (u,l) \
				in scores.items() ])
		else:
			maxscore=max(scores.values())
			if maxscore==0: maxscore=vsmall
			return dict([ (u,float(c)/maxscore) for (u,c) in scores.items() ])
	
	def frequencyscore(self,rows):
		counts=dict([ (row[0],0) for row in rows ])
		for row in rows: counts[row[0]]+=1
		return self.normalizescores(counts)
		
	def locationscore(self,rows):
		locations=dict([ (row[0], 1000000) for row in rows ])
		for row in rows:
			loc=sum(row[1:])
			if loc<locations[row[0]]: locations[row[0]]=loc
		
		return self.normalizescores(locations,smallIsBetter=1)
		
	def distancescore(self,rows):
		if len(rows[0])<=2: return dict([(row[0],1.0) for row in rows])
		
		mindistance=dict([ (row[0],100000) for row in rows ])
		
		for row in rows:
			dist=sum([abs(row[i]-row[i-1]) for i in range(2,len(row))])
			if dist<mindistance[row[0]]: mindistance[row[0]]=dist
		
		return self.normalizescores(mindistance,smallIsBetter=1)
	
	def inboundlinkscore(self,rows):
		uniquerls=set([row[0] for row in rows])
		inboundcount=dict([ (u,self.con.execute(\
			'select count(*) from link where toid=%d' %u ).fetchone()[0])  \
			for u in uniquerls ])
		
		return self.normalizescores(inboundcount)
		
	def nnscore(self,rows,wordids):
		self.mynet=nn.searchnet('data/nn.db')
		# Получить уникальные идентификаторы URL в виде упорядоченного списка
		urlids=[urlid for urlid in set([row[0] for row in rows])]
		nnres=self.mynet.getresult(wordids,urlids)
		scores=dict([(urlids[i],nnres[i]) for i in range(len(urlids))])
		return self.normalizescores(scores)
