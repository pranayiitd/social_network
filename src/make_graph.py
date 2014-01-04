import json
from pprint import pprint
import sys

def dump_row(arr):
	s =""	
	for elem in arr:
		s = s+str(elem)+","

	s = s[:len(s)-1]+"\n"
	return s

def extract_info(entry):
	s = dump_row([entry['user_id'],entry['user_name'],entry['user_lang'],entry['user_location'],entry['user_statuses_count'],entry['user_verified'],entry['user_followers_count'],entry['user_friends_count'],"1"])
	return s




# f1 = open("graph/followers.txt","r")
# f2 = open("graph/friends.txt","r")

def authors():
	f3 = open("graph/authors.txt","r")
	f = open("graph/nodes.csv","w")

	l3 = f3.readline()
	while l3 :
		e3 = json.loads(l3)
		node = extract_info(e3)
		f.write(node)
		l3 = f3.readline()

	f3.close()
	f.close()

def get_relations():
	f1 = open("graph/followers.txt","r")
	f2 = open("graph/friends.txt","r")
	followers =[]
	friends = []
	fo_set =set()
	fr_set = set()
	
	l1 = f1.readline()
	l2 = f2.readline()
	count =0
	
	while l1:
		e1 = json.loads(l1)
		e2 = json.loads(l2)
		followers = followers+ e1['followers']
		friends = friends+ e2['friends']
		count+=1
		# sys.stdout.write("\r %d"%count)

		if(count%100==0):
			print "removing duplicates",count
			fo_set = fo_set|set(followers)|set(friends)
			fr_set = fr_set|set(friends)
			followers =[]
			friends = []
		
		l1 = f1.readline()
		l2 = f2.readline()
		# break
	f1.close();f2.close()

	print len(fo_set),len(fr_set)

	authors = {}
	f = open("graph/authors.txt","r")
	l = f.readline()
	while l:
		a = json.loads(l)
		# pprint(a)
		# break
		authors[a['user_id']] =1
		l = f.readline()
	f.close()

	f_node = open("graph/nodes.csv","a")
	
	rels = list(fo_set)
	
	for i in rels:
		if(authors.has_key(i)==False):
			f_node.write(dump_row([i,"","","","","","","",0]))

def make_relations():
	
	f1 = open("graph/followers.txt","r")
	f2 = open("graph/friends.txt","r")
	f = open("graph/rel.csv","a")
	
	l1 = f1.readline()
	l2 = f2.readline()
	count =0
	
	while l1:
		e1 = json.loads(l1)
		e2 = json.loads(l2)
		author = e1['author']
		followers =  e1['followers']
		friends =  	 e2['friends']
		
		for i in followers:
			row = str(author)+","+str(i)+"follows"
			f.write(row+"\n")
		
		for j in friends:
			row = str(j)+","+str(author)+"follows"
			f.write(row+"\n")

		l1 = f1.readline()
		l2 = f2.readline()
	
		count+=1



def relations():
	authors = {}
	f = open("graph/authors.txt","r")
	l = f.readline()
	
	while l:
		a = json.loads(l)
		# pprint(a)
		# break
		authors[a['user_id']] =1
		l = f.readline()

	f.close()
	print len(authors)

# get_relations()	
# relations()

# authors()
make_relations()