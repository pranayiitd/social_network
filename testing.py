import json
from pprint import pprint

def one(f, d):
	d[1]=2
	print f.readline()

def second():
	f = open("users.txt","r")
	prof = json.loads(f.readline())
	# pprint(prof["response"])
	pprint(len(json.loads(prof["users"])))
	pprint(json.loads(prof["users"])[0]["id"] )
	# d ={}
	# one(f,d)	
	# print d
	# one(f,d)
	

second()		