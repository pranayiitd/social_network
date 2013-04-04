import os
import json
import twitter
from pprint import pprint

# COLLECTS AUTHOR DETAILS FROM THE TWEET
def get_author_details(tweet, format):
	# Will have to change as per yahoo format
	if(format=="yahoo"):
		time_zone =""
		desc = ""
		
		if(tweet['rtds_tweet'].has_key('user_time_zone')):
			time_zone = tweet['rtds_tweet']['user_time_zone']
		
		if(tweet['rtds_tweet'].has_key('user_description')):
			time_zone = tweet['rtds_tweet']['user_description']
		
		author_details ={
				"user_id" : tweet['rtds_tweet']['user_id'],
				"user_created_at" : tweet['rtds_tweet']['user_created_at'],
				"user_description" : time_zone,
				"user_followers_count" :tweet['rtds_tweet']['user_followers_count'],
				"user_friends_count"  :tweet['rtds_tweet']['user_friends_count'],
				"user_lang" : tweet['rtds_tweet']['user_lang'],
				"user_location" : tweet['rtds_tweet']	['user_location'], 
				"user_name" : tweet['rtds_tweet']['user_name'],
				"user_profile_image_url" :tweet['rtds_tweet']['user_profile_image_url'],
				"user_protected"  : tweet['rtds_tweet']['user_protected'] ,
				"user_screen_name" :tweet['rtds_tweet']['user_screen_name'],
				"user_statuses_count" :tweet['rtds_tweet']['user_statuses_count'],
				"user_time_zone" :time_zone,
				"user_utc_offset" :tweet['rtds_tweet']['user_utc_offset'],
				"user_verified"  :tweet['rtds_tweet']['user_verified'],
			}
		return author_details
		
	else:
		return tweet['user']


# Load the database of users in Dictionary
def load_users_db(loc):
	f = open(loc,"r")
	d = {}
	line = f.readline()
	while line:
		d[int(line.replace("\n",""))] = 1
		line = f.readline()
	f.close()
	return d

def get_authors(paths):
	
	dir_list = os.listdir(paths['sampled_tweets'])
	count =0
	# print dir_list
	for d in dir_list:
		
		# The source of tweets
		old_dir = paths["sampled_tweets"]+"/"+d
		file_list = os.listdir(old_dir)
		print "Reading from dir ",old_dir
		
		#New dir for dumping authors
		new_dir = paths["graph"]+"/"+d
		os.mkdir(new_dir)
		print "Created new dir ",new_dir

		for sample in file_list:
			print "    file ",sample
			fsample = open(old_dir+"/"+sample,"r")
			fauth   = open(new_dir+"/"+sample,"w")

			line = fsample.readline()
			print "TAKING AUTHORS FROM", sample	
			while line:
				tweet = json.loads(line)
				tid = twitter.get_tweetid(tweet,"yahoo")
				uid = twitter.get_uid(tweet,"yahoo")
				fauth.write(json.dumps(get_author_details(tweet,"yahoo"))+"\n")
				count+=1


				# # IF THE AUTHORS ALREADY IN DATABASE THEN IGNORE
				# if(users_db.has_key(uid)):
				# 	line = fsample.readline()
				# 	continue
				# else:
				# 	# Insert in db(both file and Dict) 
				# 	f_db.write(str(uid)+"\n")
				# 	users_db[uid] = 1
				# 	# and also in the authors.txt 
				# 	fauth.write(json.dumps(get_author_details(tweet,"yahoo"))+"\n")
					
				
				line = fsample.readline()
			
		
			fsample.close()
			fauth.close()
			

	
	# return
	# # GLOBAL DATABSAE OF ALL THE UNIQUE USERS
	# users_db = {}
	# print "loading users_db"
	# users_db = load_users_db(paths['users_db'])
	# count =0
	
	return count
	