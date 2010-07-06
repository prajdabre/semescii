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

import json


from htmlentitydefs import codepoint2name
def unicode2htmlentities(u):
    htmlentities = list()
    for c in u:
        if ord(c) < 128:
            htmlentities.append(c)
        else:
            htmlentities.append('&#%s;' % ord(c))
    return ''.join(htmlentities)

class AnimeInfo:
    def __init__(self, con):
        self.con = con
    
    def info(self, id):
        if not id: return None
        info = self.con.execute("""
            select page, description, titles, score, img  from anime
            where rowid = %d""" % id).fetchone()
        if not info: return None
           
        (engtitle, altitle, jptitle) = info[2].split(';|;')
        description = unicode2htmlentities(info[1])
        info = {
                'title': unicode2htmlentities(engtitle),
                'altitle': unicode2htmlentities(altitle),
                'jptitle': unicode2htmlentities(jptitle),
                'img': info[4], 
                'description': description, 
                'score': info[3], 
                'genres': self.__get('genre', id), 
                'urldescription': unicode2htmlentities(info[0])
        }
        return info
    
    def __get(self, name, id):
        res = self.con.execute("""
            SELECT %s_name FROM %ss
            WHERE anime_id = %d
        """ % (name, name, id)).fetchall()
        result = []
        for row in res:
            result.append(row[0])
        return result
    
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
        weights=[(0.5, self.userscore(rowid)),
                 (0.8, self.producerscore(rowid)),
                 (0.5, self.genresscore(rowid)),
                 (0.3, self.tagsscore(rowid)),
                 (0.5, self.ratingscore(rowid)),
                 (1.5, self.staffscore(rowid)),
                 (0, {0:0})]
        ids =  [scores.keys() for weight, scores in weights][0]
        for i in range(0, len(ids)):
            if ids[i] == None: ids[i] = 0
        weights[6] = (1, self.nnscore(rowid, ids))
        
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
    
    @timeit
    def staffscore(self, rowid):
        res = self.con.execute("""
                 SELECT anime_id FROM anime_positions
                     WHERE people_id = (
                     SELECT people_id FROM anime_positions
                     WHERE anime_id = %d
                 )
            UNION 
                 SELECT anime_id FROM anime_acting_roles
                     WHERE people_id = (
                     SELECT people_id FROM anime_positions
                     WHERE anime_id = %d
                 )
        """ % (rowid, rowid)).fetchall()
        result = {}
        for row in res:
            try:
                result[row[0]] = +1
            except KeyError:
                result[row[0]] = 1
        return self.normalizescores(result)

    
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
        res = self.con.execute("""
            SELECT t1.anime_id, COUNT(t1.producer_name) as cnt FROM producers t1
            WHERE t1.producer_name IN
               (SELECT t2.producer_name FROM producers t2
                WHERE t2.anime_id = %d)
            GROUP BY t1.anime_id
        """ % rowid ).fetchall()
        result = {}
        for row in res:
            result[row[0]] = row[1]
        return self.normalizescores(result)

    @timeit
    def genresscore(self, rowid):
        res = self.con.execute("""
            SELECT t1.anime_id, COUNT(t1.genre_name) as cnt  FROM genres t1
            WHERE t1.genre_name IN
               (SELECT t2.genre_name FROM genres t2
                WHERE t2.anime_id = %d)
            GROUP BY t1.anime_id
        """ % rowid ).fetchall()
        result = {}
        for row in res:
            result[row[0]] = row[1]
        return self.normalizescores(result)
        
    def genrennscore(self, rowid):
        pass
    

    def animelikecrawlernetscore(self, rowid):
        pass
        
    @timeit
    def tagsscore(self, rowid):
        res = self.con.execute("""
            SELECT t1.anime_id, COUNT(t1.tag_name) as cnt  FROM tags t1
            WHERE t1.tag_name IN
               (SELECT t2.tag_name FROM tags t2
                WHERE t2.anime_id = %d)
            GROUP BY t1.anime_id
        """ % rowid ).fetchall()
        result = {}
        for row in res:
            result[row[0]] = row[1]
        return self.normalizescores(result)
        
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
