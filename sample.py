import os

def random_sample(paths):

	filtered_files = os.listdir(paths['filtered_tweets'])
	SIZE = 50
	total_count =0
	# Taking SIZE number of tweets from every file

	for raw_file in filtered_files:
		print "sampling ", raw_file
		cmd = "head -"+str(SIZE)+" "+paths['filtered_tweets']+"/"+raw_file+" > "+paths['sampled_tweets']+"/"+raw_file
		os.system(cmd)
		total_count+=SIZE

		# fraw = open(,"r")
		# fdest = open(paths['sampled_tweets']+"/"+raw_file,"w")

		# line = fraw.readline()
		# count =0
		# while line:
		# 	if(count==SIZE):
		# 		break
		# 	fdest.write(line)
		# 	total_count+=1
		# 	line = fraw.readline()
		# 	count+=1
		# fraw.close()
		# fdest.close()
	return total_count
	