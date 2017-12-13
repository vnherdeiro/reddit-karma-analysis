#! /usr/bin/python

import re
import urllib2
from Queue import Queue
import pickle
from time import sleep
from socket import gethostname
from random import choice
from sys import argv

#update this to python3 plus parsing with BS4

hostname = gethostname()
infile = argv[1]
outfile = infile
#CriticalMass = 10000 #upper boundary on the user Queue mass

baseUrl = "http://www.reddit.com/user/"
users = Queue()
userSet = set()

#with open(infile,"r") as f:
#	results = pickle.load(f)
with open(infile,"r") as f:
	dat = [line.rstrip("\n").split() for line in f.readlines()]
results = {user:int(karma) for user, karma in dat}
del dat
user0 = choice(results.keys())
print user0
users.put(user0)
userSet |= set(results.keys())

#renaming
while not users.empty():
	user = users.get()
	try:
		request = urllib2.Request( baseUrl + user, headers= {'User-agent': 'Mozilla/5.0'})
		raw_dat = urllib2.urlopen( request).read()
	except:
		print "\t\trejection..."
		sleep(5)
	#read karma here
	else:
		ind = raw_dat.find("comment-karma")
		substr = raw_dat[ind:ind+60]
		substr = substr[substr.find(">")+1:substr.find("<")]
		karma = "".join([_ for _ in substr if _.isdigit()])
		karma = int(karma)
		print user,"\t",karma
		results[user] = karma
		with open(outfile,"a") as f:
			f.write("%s %d\n" %(user,karma))

		new_users = re.findall("user\/(\w+)", raw_dat)
		#new_users = map(lambda _ : _[5:],new_users)
		new_users = {_ for _ in new_users if _ not in userSet}
		userSet |= new_users
		#while new_users and users.qsize() <= CriticalMass:
		#	users.put(new_users.pop()) #NOT WORKING BECAUSE WE ADDED ALL THE USERS TO THE SET
			#IMPLEMENT IF REALLY NEEDED (QUEUE GROWS TOO LARGE)
		for _ in new_users:
			users.put(_)
	#sleep(1) #TRYING NO DELAY THIS TIME

print "Queue emptied!"

#EOF
