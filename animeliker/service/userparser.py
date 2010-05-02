from BeautifulSoup import BeautifulSoup
import urllib2
import cPickle

def getUserAnimeScore(username):
	soup = BeautifulSoup( urllib2.urlopen("http://myanimelist.net/animelist/"+username) )
	
	userAnimeScore = {}
	result = soup.findAll('a', title="Anime Information");
	for item in result:
		table = item.parent.parent
		
		animeName = str(item.contents[0].contents)
		animeScore = str(table.contents[5].contents[0])
		try:
			animeScore = int(animeScore)
		except: 
			continue
			
		userAnimeScore[animeName] = animeScore
		
	return userAnimeScore


users = ["Cirion", "aero151", "Kipcha", "Thetwinmeister", "Tyvl", "nikici", "0m3g413", "rin777",
		 "kilbiller", "momokuro", "Spade", "SuperLoop", "SuperLoop", "Oosran", "docmarionum1", "Geosunrise",
		 "Surtic", "InconVenious", "Takala", "Takala", "Spauke", "lukimba", "animefan88", "Mimeiko",
		 "jkun", "djhot", "Crystal", "Xinil", "Aokaado", "Crystal", "Arcane", "Ufozile", "vondur", 
		 "Amuro", "Baman", "megan", "Koreth", "kei-clone", "seif", "Ladholyman", "Kuningaspultti",
		 "Smoka", "Zekkai", "marvin_9martian", "Hiromi", "Cruzle", "Blaedfire", "koalatees",
		 "Ramp", "Achtor", "astrasoul7", "wicked2k", "Ravell", "manny22", "LostF", "Vaknyk", 
		 "akagi111", "saia", "THeMooN", "SunaoWolfie", "Pralyn", "Pralyn", "_edge_", "MoeMoeKyun",
		 "moridin84", "odst01", "technokid", "OKkuammiei", "FiiFO", "Luka-tan", "JHB", "Whathead", 
		 "iconoclast89", "cooldonner", "Fujibayashi", "Mamoru-kun", "_Isaac_", "KuroNoDemian",
		 "Yetmyit", "Mentaur", "JayToTheLu", "RenaPsychoKiller", "Pikena", "JayToTheLu", 
		 "WolFRAHMM", "kwakka", "Rhodo", "TaizenKyo", "xecutioners", "Sgt_Grobinov", "Tokumei",
		 "CardboardO-San", "EagleW", "Rizziks", "city-of-light", "Noein-Disgaea", "Leclerq", "Vinhthehero",
		 "Oya-tama", "Mion-chan", "Fawilia", "DarkElve", "Fallout", "airthemovie", "Wasabi", 
		 "Valerynn", "Gurenn", "Seight", "Saamoot", "melisa_hp", "wassay", "CloudedMinds", "Phanessa",
		 "Chaska", "tenshim", "Waterstar", "Neturan", "plop", "Tenshi", "Prinz_Eugen", 
		 "Ishiyumi", "Yuzuyu-chan", "moshi_moshi", "TheSlinger", "Xelotath", "Feya", "TheVOid",
		 "hollowRukia", "fez", "Cgan", "Godless", "TheGregster", "Surtic", "snake_123", "DiNeRo",
		 "BBlaXe", "Sarah-chan", "Zuminori", "Cirn9", "Ken-san", "Sniz", "Verray", "Ari-san", 
		 "Neon911", "Yukine", "msun", "Laena", "KravenErgeist", "Patrikki", "KhakiBlueSocks", 
		 "mel", "Major_G", "Acid", "2Bfreeyumi", "Akarra", "Akselerator", "Alexeon", "AndoMC",
		 "angelronin", "AniMeFreaK", "Animenia", "Annubis", "Bankai0010", "Asuka-san", "Armandthevampire", 
		 "Geese", "droesk", "Duoheero", "eL_marco", "ksenolog", "jukugo", "Laena", "Lena_chan", "Archerko",
		 "acDev", "Aoko", "andrelimfj", "Akai_Aoi", "bakatabibito", "BasseLive", "Banpaia", "bran", 
		 "bogdee_z", "Kirukato", "SWAsp1", "Kanashimi", "Sachi-chan", "4lter3go"]


file = "../data/usersAnimeScores.txt"		 
usersAnimeScores = cPickle.load( open(file, 'r') )
		 
for user in users:
	if user not in usersAnimeScores: 
		print "Indexing user: %s" % user
		usersAnimeScores[user] = getUserAnimeScore(user)

		cPickle.dump(usersAnimeScores, open(file, 'w'))
