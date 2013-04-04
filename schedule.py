import os
from datetime import datetime

import sample
import get_authors
import get_followers
import get_fids
import get_profiles
import get_friends

def dump_log(loc, arr):
	f = open(loc,"a")
	s =""	
	for elem in arr:
		s = s+str(elem)+"\t"
	s = s+"\n"
	f.write(s)
	f.close()

# /home/y/var/timesense/data/twitter_filteredTweets/en-US/syc

paths = {	"filtered_tweets" :"../tweets_dump",
			"sampled_tweets" :"../sample_dump",
			"graph" : "../graph/2013-04-03",
			"users_db"   : "../graph/users_db.txt",

			"sampling_log" : "../graph/sampling_log.txt",
			"authors_log" :"../graph/authors_log.txt",
			"followers_log" : "../graph/followers_log.txt",
			"profiles_log" : "../graph/profiles_log.txt",
			"friends_log" : "../graph/friends_log.txt",
			
			}


# ret = sample.random_sample(paths)
# dump_log(paths['sampling_log'], [ paths['sampled_tweets'], datetime.now(), ret])

# ret = get_authors.get_authors(paths)
# dump_log(paths['authors_log'], [ paths['sampled_tweets'], datetime.now(), ret])

# ret = get_followers.start(paths)
# dump_log(paths['followers_log'], [ paths['sampled_tweets'], datetime.now(), ret])

ret = get_friends.start(paths)
dump_log(paths['profiles_log'], [ paths['graph'], datetime.now(), "profiles", ret])

# ret = get_fids.get_fids(paths)
# dump_log(paths['followers_log'], [ paths['graph'], datetime.now(), "new fids", ret])

# ret = get_profiles.start(paths)
# dump_log(paths['profiles_log'], [ paths['graph'], datetime.now(), "profiles", ret])

