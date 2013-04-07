import json
import sys
import os

paths = {	"filtered_tweets" :"../tweets_dump",
			"sampled_tweets" :"../sample_dump/2013-03-29",
			"graph" : "../graph/2013-03-29",
			"users_db"   : "../graph/users_db.txt",

			"sampling_log" : "../graph/sampling_log.txt",
			"authors_log" :"../graph/authors_log.txt",
			"followers_log" : "../graph/followers_log.txt",
			"profiles_log" : "../graph/profiles_log.txt",
			
			}

def count_authors():

	f1 = open("../graph/2013-04-03/authors.txt","r")
	f2 = open("../graph/2013-04-04/authors.txt","r")

	# f1 = open("../graph/temp/authors.txt","r")
	# f2 = open("../graph/temp/authors.txt","r")

	arr =[]
	
	line = f1.readline()
	while line:
		entry = json.loads(line)
		uid = entry["user_id"]
		arr.append(uid)
		line = f1.readline()


	line = f2.readline()
	while line:
		entry = json.loads(line)
		uid = entry["user_id"]
		arr.append(uid)
		line = f2.readline()

	f1.close()
	f2.close()
	print "Total\tUnique\tPercentage"
	y = len(arr)
	x = len(set(arr))

	print "%d\t%d\t%0.2f"%(y,x,100*x/y)

def count_friends():
#	f = open(paths["graph"]+"/followers.txt","r")
        f= open("../visualize/data/friends.txt","r")
        line = f.readline()
	followers_count =0
	followers =[]
	while line:
		entry = json.loads(line)
		followers = followers+entry['friends']
		# count = len(set(entry['followers']))
		# followers_count+=count
		# print len(entry['followers'])
		line =f.readline()
	return len(set(followers))




def count_followers():
#	f = open(paths["graph"]+"/followers.txt","r")
        f= open("../visualize/data/followers.txt.head","r")
        line = f.readline()
	followers_count =0
	followers =[]
	while line:
		entry = json.loads(line)
		followers = followers+entry['followers']
		# count = len(set(entry['followers']))
		# followers_count+=count
		# print len(entry['followers'])
		line =f.readline()
	return len(followers), len(set(followers))


def count_users():
	f = open(paths["graph"]+"/profiles.txt","r")
	line = f.readline()
	users_count =0
	users =[]
	while line:
		entry = json.loads(line)
		users_count+=len(json.loads(entry['users']))

		# count = len(set(entry['followers']))
		# followers_count+=count
		# print len(entry['followers'])
		line =f.readline()
	
	return users_count

def count_uids():
	f = open(paths["graph"]+"/fids_new.txt","r")
	line = f.readline()
	count =0
        fids=[]
	while line:
		entry = json.loads(line)
		fids = fids+entry
		line = f.readline()
	return len(set(fids))

def count_trending_tweets():
	files = os.listdir("../india/tweets")
	count =0
	for i in range(len(files)):
		f = open("../india/tweets/"+files[i],"r")
		line = f.readline()
		while line:
			entry = json.loads(line)
			tweets = json.loads(entry['tweets'])
			count = count+len(tweets['statuses'])
			# break
			line = f.readline()
		# break
	return count

cmd = sys.argv[1]

if(cmd=="u" or cmd=="a"):
	print "Number of profiles collected ",count_users()

if (cmd=="f" or cmd=="a"):
	print "Number of total followers ids ",count_followers()

if (cmd=="fr" or cmd=="a"):
	print "Number of total friends ids ",count_friends()


if (cmd=="ua" or cmd=="a"):
	print "Number of Unique followers ids ",count_uids()

if (cmd=="auth" or cmd=="a"):
	count_authors()

# if (cmd=="tt" or cmd=="a"):	
# 	print count_trending_tweets()
