from math import sqrt

#класс для подсчета схожести аниме по рейтингам пользователей
class UserRecommendations:
	def __init__(self, prefs):
		self.prefs = prefs
	
	def __del__(self):
		pass
	
	#возвращает схожесть интересов по Евклидовому расстоянию
	def sim_distance(self, person1,person2):
		si={}
		for item in self.prefs[person1]:
			if item in self.prefs[person2]:
				si[item]=1
		if len(si)==0: return 0
		
		sum_of_squares=sum([pow(self.prefs[person1][item]-self.prefs[person2][item],2)
		for item in self.prefs[person1] if item in self.prefs[person2]])
		return 1/(1+sum_of_squares)

	#возвращает схожесть интересов по алгоритму Пирсона
	def sim_pearson(self, p1,p2):
		si={}
		for item in self.prefs[p1]:
		    if item in self.prefs[p2]: si[item]=1
		n=len(si)
		if n == 0: return 0
		
		sum1=sum([ self.prefs[p1][it] for it in si ])
		sum2=sum([ self.prefs[p2][it] for it in si ])
		
		sum1Sq=sum([ pow(self.prefs[p1][it],2) for it in si ])
		sum2Sq=sum([ pow(self.prefs[p2][it],2) for it in si ])
		
		pSum=sum([ self.prefs[p1][it]*self.prefs[p2][it] for it in si ])
		
		#Pearson coficent
		num=pSum-(sum1*sum2/n)
		den=sqrt( ( sum1Sq-pow(sum1,2)/n ) * ( sum2Sq-pow(sum2, 2) / n ) )
		
		if den==0: return 0
		
		r=num/den
		return r

	# Возвращает список наилучших соответствий для человека из словаря prefs.
	def topMatches(self, person, n=10):
		try:
			self.prefs[person]
		except KeyError:
			return {}
		
		scores=[]
		for other in self.prefs:
			if other==person: continue
			score = self.sim_pearson(person,other)
			if score > 0:
				scores.append([score, other])
		
		scores.sort()
		scores.reverse()
		
		res = {}
		for (score, name) in scores:
			res[name] = score
		return res


	# Получить рекомендации для заданного человека, пользуясь взвешенным средним
	# оценок, данных всеми остальными пользователями
	def getRecommendations(self, person):
		totals={}
		simSums={}
		for other in self.prefs:
			if other==person: continue
			sim=self.sim_pearson(self.prefs,person,other)
		
			if sim <= 0: continue
			
			for item in self.prefs[other]:
				if item not in self.prefs[person] or self.prefs[person][item]==0:
					totals.setdefault(item,0)
					totals[item]+=self.prefs[other][item]*sim
					
					simSums.setdefault(item,0)
					simSums[item]+=sim
			
		rankings=[(total/simSums[item],item) for item, total in totals.items( )]
		
		rankings.sort()
		rankings.reverse()
		return rankings


		
def transformPrefs(prefs):
	result={}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})
			
			# Обменять местами человека и предмет
			result[item][person]=prefs[person][item]
	return result



