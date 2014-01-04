import json
from pprint import pprint

f1 = open("followers.txt","r")
f2 = open("friends.txt","r")

d1 ={};d2={}


for i in range(1700):
	l1 = f1.readline()
	l2 = f2.readline()
	e1 = json.loads(l1)
	e2 = json.loads(l2)

	if(d1.has_key(e1['author'])==False):
		d1[e1['author']] = e1
	if(d2.has_key(e2['author'])==False):
		d2[e2['author']] = e2
	
f1.close()
f2.close()

print len(d1),len(d2)

f = open("authors.txt","r")

f1 = open("graph/followers.txt","w")
f2 = open("graph/friends.txt","w")
f3 = open("graph/authors.txt","w")

l = f.readline()
authors ={}

while l:
	e = json.loads(l)
	uid = e['user_id']
	
	if(d1.has_key(uid) and d2.has_key(uid) and authors.has_key(uid)==False):
		authors[uid] =1
		f1.write(json.dumps(d1[uid])+"\n")
		f2.write(json.dumps(d2[uid])+"\n")
		f3.write(json.dumps(e)+"\n")

	l = f.readline()

