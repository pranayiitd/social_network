import os
import json
import oauth2 as oauth
from pprint import pprint
from datetime import datetime
import time

import twitter

def load_users_db(loc):
	f = open(loc,"r")
	d = {}
	line = f.readline()
	while line:
		d[int(line.replace("\n",""))] = 1
		line = f.readline()
	f.close()
	return d

def insert_new(arr, users_db, users_db_path):

	f = open(users_db_path,"a")
	for user in arr:
		fid = user["id"]
		if(users_db.has_key(int(fid))):
			continue
		else:
			users_db[int(fid)] =1
			f.write(str(fid)+"\n")
	f.close
	# return new_arr


def dump_log(loc, arr):
	f = open(loc,"a")
	s =""	
	for elem in arr:
		s = s+str(elem)+"\t"
	s = s+"\n"
	f.write(s)
	f.close()

def find_start(dest, source):
	profiles_dump = dest
	fids_dump = source

	ff = open(dest,"r")
	flines = ff.readlines()
	last_id=""
	
	n =len(flines)
	for i in range(n):
		entry = json.loads(flines[n-i-1])
		users = json.loads(entry["users"])
		# Last non-empty response in the destination dumping file
		if(len(users)!=0):
			last_id = users[0]["id"]
			break
	ff.close()

	# Fiding line number in the source file containing the last_tid
	fr = open(source,"r")
	line = fr.readline()
	count =0;start_line=0
	while line:
		count+=1
		entry = json.loads(line)
		_id =entry[0]
		
		if(last_id in entry):
			start_line = count
			break
		line = fr.readline()
	
	fr.close()
	return start_line


def get_profiles(version, app, f_ids, f_profiles, users_db, users_db_path):

	CONSUMER_KEY = app['c_key']
	CONSUMER_SECRET = app['c_sec']
	ACCESS_KEY = app['a_key']
	ACCESS_SECRET = app['a_sec']
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token)
	
	ret =0;count =0;limit=0

	line = f_ids.readline()
	while line:
		users = json.loads(line)
		
	# GETTING PROFILES FROM TWITTER BY IDS
		entry = twitter.get_user_details_batch(users,0,version,client)
		insert_new(json.loads(entry["users"]), users_db, users_db_path)
		
		if(version==1):
			limit = int(entry['response']['x-ratelimit-remaining'])
		else:
			limit = int(entry['response']['x-rate-limit-remaining'])
		if(limit<3):
			endtime = datetime.now()
			ret =1
			print "limit reached"
			break

	# DUMP PROFILES
		f_profiles.write(json.dumps(entry)+"\n")	
		count+=1
		line = f_ids.readline()

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
	
	# Source of ID of users profiles to be collected
	f_ids = open(paths['graph']+"/fids_new.txt","r")
	f_profiles = open(paths['graph']+"/profiles.txt","a")
	users_db = load_users_db(paths["users_db"])
	#----------------------------------
	# Skipping the lines to start from right place.
	start_from = find_start(paths['graph']+"/profiles.txt", paths['graph']+"/fids_new.txt")
	
	print "STARTING TO READ IDS FROM LINE ", start_from
	
	return
	line=""
	for i in range(start_from):
		line = fnewAuth.readline()
	#----------------------------------
	
	i = 0 ; v = 1 ; time_elapsed = 0
	while(True):
		print "Trying version %.1f, App number %d"%(v, i)
		ret, limit, count = get_profiles(v, set_app[i], f_ids, f_profiles, users_db, paths["users_db"])
		dump_log(paths['profiles_log'],[paths['graph'], datetime.now(), ret, count])
		# All Authors followers Done
		if ret==2:
			print "ALL IDS DONE"
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
	f_ids.close()
	f_profiles.close()
	