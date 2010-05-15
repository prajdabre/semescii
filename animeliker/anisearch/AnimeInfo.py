# -*- coding: utf-8 -*-
from django.utils.encoding import smart_str, smart_unicode
from operator import itemgetter
import cPickle
from re import escape

import UserRecommendations
import SearchNet
from database.Database import Database
from database.SqliteDriver import SqliteDriver
from testing.timeit import timeit

class AnimeInfo:
    def __init__(self, con):
        self.con = con
    
    def info(self, id):
        try:
            return self.con.execute("select * from anime where rowid = %d" % id).fetchone()
        except:
            return False
    
    def getId(self, anime):
        try:
            res=self.con.execute('select rowid, titles from anime where titles LIKE ?', ('%' + anime + '%',)).fetchall()
        except IndexError:
            return None
        for row in res:
            title = row[1].split(';|;')[0]
            if title == anime:
                return int(row[0])
            
    
    def getsimilarity(self,movie1, movie2):
        id2=self.getId(movie2)
        scoredlist = self.getscoredlist(movie1)
        for item in scoredlist:
            (anime, score) = item
            if (anime==id2): return score
   
    def getscoredlist(self,rowid):
        weights=[(1.0, self.userscore(rowid)),
                 (1.0, self.producerscore(rowid)),
                 (1.5, self.genresscore(rowid)),
                 (0.5, self.tagsscore(rowid)),
                 (0.5, self.ratingscore(rowid)),
                 (0, {0:0})]
        ids =  [scores.keys() for weight, scores in weights][0]
        for i in range(0, len(ids)):
            if ids[i] == None: ids[i] = 0
        weights[5] = (2.0, self.nnscore(rowid, ids))
        
        totalscores = {}
        for (weight, scores) in weights:
            for movie in scores:
                try:
                    totalscores[movie]+=weight*scores[movie]
                except: 
                    totalscores[movie]=weight*scores[movie]
        return sorted(totalscores.items(), key=itemgetter(1), reverse=True)



    def normalizescores(self,scores,smallIsBetter=0):
        if (len(scores) == 0):
            return {}
        
        vsmall=0.00001
        if smallIsBetter:
            minscore=min(scores.values())
            return dict([ (u,float(minscore)/max(vsmall,l)) for (u,l) \
                in scores.items() ])
        else:
            maxscore=max(scores.values())
            if maxscore==0: maxscore=vsmall
            return dict([ (u,float(c)/maxscore) for (u,c) in scores.items() ])
    
    @timeit
    def userscore(self, rowid):        
        p = cPickle.loads( open("/var/www/data/userscoresfliped.txt", 'r').read() )
        r = UserRecommendations.UserRecommendations( p )
        return self.normalizescores(r.topMatches(rowid))
    
    def staffscore(self, rowid):
        pass
    
    @timeit
    def ratingscore(self, rowid):
        score = self.con.execute("SELECT score FROM anime WHERE rowid=%d" % rowid).fetchone()[0]
        rows = self.con.execute("SELECT rowid, score FROM anime WHERE score < %s + 1 AND score > %s - 1"
                                % (score, score) )
        res = {}
        for row in rows:
            res[row[0]] = score-row[1]
        return self.normalizescores(res, smallIsBetter=True)
    
    @timeit
    def producerscore(self, rowid):
        cur = self.con.execute("SELECT producers FROM anime WHERE rowid=%d" % rowid)
        producers = cur.fetchone()[0].split(';|;')
        
        res = {}
        rows = self.con.execute("SELECT rowid FROM anime WHERE producers LIKE '%"+producers[0]+"%'").fetchall()
        for row in rows:
            res[row[0]] = 1
        return self.normalizescores(res)
    
    @timeit
    def genresscore(self, rowid):
        cur = self.con.execute("SELECT genres FROM anime WHERE rowid=%d" % rowid)
        genres = cur.fetchone()[0].split(';|;')
        
        res = {}
        for genre in genres:
            rows = self.con.execute("SELECT rowid FROM anime WHERE genres LIKE ? AND rowid != ?", ('%'+genre+'%',rowid,) ).fetchall()
            for row in rows:
                try:
                    res[row[0]] += 1
                except:
                    res[row[0]] = 1
        return self.normalizescores(res)
        
    def genrennscore(self, rowid):
        pass
    

    def animelikecrawlernetscore(self, rowid):
        pass
        
    @timeit
    def tagsscore(self, rowid):
        cur = self.con.execute("SELECT tags FROM anime WHERE rowid=%d" % rowid)
        tags = cur.fetchone()[0].split(';|;')
        
        res = {}
        rows = self.con.execute("SELECT rowid FROM anime WHERE tags LIKE ? AND rowid != ?", ('%'+tags[0]+'%',rowid,) ).fetchall()
        for row in rows:
            res[row[0]] = 1
        return res
        
    @timeit    
    def nnscore(self, rowid, ids):
        mynet=SearchNet.SearchNet(
            Database(SqliteDriver('/var/www/data/nn.db'))
        )
        nnres = mynet.getresult([rowid],ids)
        scores=dict([(ids[i],nnres[i]) for i in range(len(ids))])
        return self.normalizescores(scores)
                
    def sortDict(self, adict):
        rdict = dict([(v, k) for (k, v) in adict.iteritems()])
        keys = rdict.keys()
        keys.sort()
        return map(rdict.get, keys)

