import json
from pprint import pprint

def relation(loc, typ):
	
	# a : #  < 10
	# b : #  < 30
	# c : #  < 50
	# d : #  < 100
	# e : #  < 3000

	dist ={
		"a":0,
		"b":0,
		"c":0,
		"d":0,
		"e":0,
		"celeb":0,
		}

	ff = open(loc,"r")
	line = ff.readline()
	while line:
		entry = json.loads(line)
		f = len(entry[typ])
		
		key ="celeb"
		if(f<10):
			key = "a"
		elif(f<30):
			key = "b"
		elif(f<50):
			key = "c"	
		elif(f<100):
			key = "d"
		elif(f<3000):
			key = "e"

		dist[key] = dist[key]+1
		line = ff.readline()

	ff.close()

	pprint(json.loads(json.dumps(dist)))

relation("followers.txt","followers")	