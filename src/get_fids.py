import json,pprint
import datetime

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

def remove_old(arr, users_db):
	new_arr=[]
	for fid in arr:
		if(users_db.has_key(int(fid))):
			continue
		else:
			new_arr.append(fid)
			

	return new_arr

def get_fids(paths):
	print datetime.datetime.now()

	followers_dump = paths["graph"]+"/followers.txt"
	uids = paths["graph"]+"/fids_new.txt"

	users_db = load_users_db(paths["users_db"])
	print "loaded users_db size",len(users_db)
	
	f = open(followers_dump,"r")
	fu =open(uids,"w")

	line = f.readline()
	f_set =[]

	print "READING THE FOLLOWERS IDS"
	total = 0
	while line:
		entry = json.loads(line)
		# f_set = f_set|set(entry['followers'])
		total = total +len(entry['followers'])
		f_set = f_set + remove_old(entry['followers'], users_db)
		line = f.readline()

	f_arr = list(set(f_set))

	i=0

	print "DUMPING ONLY THE NEW FIDS # %d from total fetched ids # %d"%(len(f_arr),total)
	while(i <len(f_arr)):
		end = i+100
		if(end>len(f_arr)):
			end =len(f_arr)	
		fu.write(json.dumps(f_arr[i:end])+"\n")
		i+=100

	print datetime.datetime.now()

	return len(f_arr)
	
