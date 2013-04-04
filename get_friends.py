import os
import json
import oauth2 as oauth
from pprint import pprint
from datetime import datetime
import time

import twitter

def dump_log(loc, arr):
	f = open(loc,"a")
	s =""	
	for elem in arr:
		s = s+str(elem)+"\t"
	s = s+"\n"
	f.write(s)
	f.close()

def find_start(dest, source):
	friends_dump = dest
	followers_tweet = source

	ff = open(dest,"r")
	flines = ff.readlines()
	last_id=""
	
	n =len(flines)
	for i in range(n):
		entry = json.loads(flines[n-i-1])
		# Last non-empty response in the destination dumping file
		if(len(entry["friends"])!=0):
			last_id = entry['author']
			break
	ff.close()

	# Fiding line number in the source file containing the last_tid
	fr = open(source,"r")
	line = fr.readline()
	count =0;start_line=0
	while line:
		count+=1
		entry = json.loads(line)
		_id =entry["author"]
		
		if(_id==last_id):
			start_line = count
			break
		line = fr.readline()
	
	fr.close()
	return start_line


def get_friends(version, app, f1, f2):

	CONSUMER_KEY = app['c_key']
	CONSUMER_SECRET = app['c_sec']
	ACCESS_KEY = app['a_key']
	ACCESS_SECRET = app['a_sec']
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token)
	
	ret =0;count =0;limit=0

	# uid = "117373597"
	# entry = twitter.get_followers(uid,0,version,client)
	# print entry
	
	# entry = twitter.get_friends(uid,0,version,client)
	# print entry
	
	# return [ret, limit, count]

	line = f1.readline()
	while line:
		entry = json.loads(line)
		uid = entry['author']
		
	# 	#GETTING FOLLOWERS FROM TWITTER by user_id
		entry = twitter.get_friends(uid,0,version,client)
		
		if(version==1):
			limit = int(entry['response']['x-ratelimit-remaining'])
		else:
			limit = int(entry['response']['x-rate-limit-remaining'])
		if(limit<3):
			endtime = datetime.now()
			ret =1
			print "limit reached"
			break
	# 	DUMP FRIENDS IDs
		f2.write(json.dumps(entry)+"\n")	
		count+=1

		line = f1.readline()

	# BREAKING LOOP BECAUSE FILES IS COMPLETE
	if(limit >=3):
		ret =2
	return [ret, limit, count]


def start(paths):

	fapp = open('twitter_app.txt',"r")
	lines = fapp.readlines()
	set_app =[]; i=0
	while (i+3)<(len(lines)):
		app = {}
		app['c_key'] = lines[i].replace("\n","")
		app['c_sec'] = lines[i+1].replace("\n","")
		app['a_key'] = lines[i+2].replace("\n","")
		app['a_sec'] = lines[i+3].replace("\n","")
		set_app.append(app)
		i+=5
	
	# Source of authors whose followers to be collected
	f1 = open(paths['graph']+"/followers.txt","r")
	f2 = open(paths['graph']+"/friends.txt","a")
	
	#----------------------------------
	# Skipping the lines to start from right place.
	start_from = find_start(paths['graph']+"/friends.txt", paths['graph']+"/followers.txt")
	print "starting to read authors from line ", start_from
	
	# return
	
	line=""
	for i in range(start_from):
		line = f1.readline()
	#----------------------------------
	
	i = 0 ; v = 1 ; time_elapsed = 0
	while(True):
		print "Trying version %.1f, App number %d"%(v, i)
		ret, limit, count = get_friends(v, set_app[i], f1, f2)

		dump_log(paths['friends_log'],[paths['graph'], datetime.now(), ret, count])
		
		# All Authors followers Done
		if ret==2:
			print "ALL AUTHORS DONE"
			break
		# Try different app combination
		if(limit<3):
			print "TRYING ANOTHER COMBINATION"
			if(i<3):
				i+=1
			else:
				if(v==1):
					v=1.1
					i=0
				else:
					print "GOING TO SLEEP NOW FOR 15 MINS FROM ",datetime.now()
					time.sleep(15*60)
					time_elapsed +=15
					i=0
					if(time_elapsed>=60):
						v=1
						time_elapsed=0
	f1.close()
	f2.close()