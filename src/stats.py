import json
import sys
import os
from pprint import pprint

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

def count_all():
	

	total_authors =0
	total_followers =0
	total_friends =0
	total_r1 =0.0
	total_r2 =0.0
	zero =0

	f= open("../visualize/data/authors.txt","r")
	line = f.readline()
	
	while line:
		entry = json.loads(line)
		x = entry['user_followers_count']
		y = entry['user_friends_count']
		# print x,y
		# break
		if(x==0 or y==0):
			zero+=1
			line = f.readline()
			continue
		
		total_authors+=1
		total_followers+=x
		total_friends+=y
		total_r1 += (y/x)
		total_r2 += (x/y)
			
		#sys.stdout.write("\r count :"+str(total_authors))
		line = f.readline()

	r1 = float(total_r1)/total_authors
	r2 = float(total_r2)/total_authors
	print "count, Followers, Friends \t R \t r1 \t r2"
	print "%d, %d, %d \t %0.2f \t %0.2f \t %f"%(total_authors,total_followers,total_friends,float(total_friends)/total_followers,r1,r2)
	print "Average Followers",total_followers/total_authors
	print "Average Friends ",total_friends/total_authors
	print zero
	# return count


def count_friends():
 	f= open("../visualize/data/friends.txt","r")
 	line = f.readline()
	followers_count =0
	followers =[]
	while line:
		entry = json.loads(line)
		#followers = followers+entry['friends']
		count = len((entry['friends']))
		followers_count+=count
		# print len(entry['followers'])
		line =f.readline()
#	return len(set(followers))
        return followers_count



def count_followers():
#	f = open(paths["graph"]+"/followers.txt","r")
        f= open("../visualize/data/followers.txt","r")
        line = f.readline()
	followers_count =0
	followers =[]
	while line:
		entry = json.loads(line)
		#followers = followers+entry['followers']
		count = len((entry['followers']))
		followers_count+=count
		# print len(entry['followers'])
		line =f.readline()
#	return len(followers), len(set(followers))
        return followers_count

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
	#f = open(paths["graph"]+"/fids_new.txt","r")
	f= open("../visualize/data/followers.txt","r")
	line = f.readline()
	count =0

	total_f =0
	fids = []
	followers=set()
	while line:
		entry = json.loads(line)
		total_f += len(entry['followers'])
		fids = fids + entry['followers']
		count+=1
		# print count
		if(count%100==0):
			followers = followers|set(fids)
			fids =[]# x = len(set(fids))
			x = len(followers)
			y = total_f
			# y = len(fids)
			print "%d, %d, %d, %f, %d"%(count,y,x,float(x)/y,y/count)

		line = f.readline()
        
  	f.close()
	return len(set(fids))

def count_trending_tweets():
	files = os.listdir("../india/tweets")
	total_authors =0
	total_followers =0
	total_friends =0
	total_r1 =0.0
	total_r2 =0.0
	zero =0
	for i in range(len(files)):
		f = open("../india/tweets/"+files[i],"r")
		line = f.readline()
		while line:
			entry = json.loads(line)
			tweets = json.loads(entry['tweets'])
			
			for j in range(len(tweets['statuses'])):
				x = tweets['statuses'][j]['user']['followers_count']
				y = tweets['statuses'][j]['user']['friends_count']
				if(x==0 or y==0):
					zero+=1
					continue
				total_authors+=1
				total_followers+=x
				total_friends+=y
				total_r1 += (y/x)
				total_r2 += (x/y)
                        #print total_authors				
			line = f.readline()
		# break
	r1 = float(total_r1)/total_authors
	r2 = float(total_r2)/total_authors
	print "count, Followers, Friends \t R \t r1 \t r2"
	print "%d, %d, %d \t %0.2f \t %0.2f \t %f"%(total_authors,total_followers,total_friends,float(total_friends)/total_followers,r1,r2)
	print "Average Followers",total_followers/total_authors
	print "Average Friends ",total_friends/total_authors
	print zero
	# return count

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

if (cmd=="tt" or cmd=="a"):	
	count_trending_tweets()

if (cmd=="all" or cmd=="a"):	
	count_all()
