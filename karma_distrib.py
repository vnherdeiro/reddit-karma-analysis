#! /usr/bin/python3

import re
import urllib
import urllib.request
from queue import Queue
#from bs4 import BeautifulSoup as bs
import pickle
from time import sleep
from random import choice
from sys import argv

#update this to python3 plus parsing with BS4

infile = argv[1]
outfile = infile
#CriticalMass = 10000 #upper boundary on the user Queue mass

baseUrl = "http://www.reddit.com/user/"
users = Queue()
userSet = set()

with open(infile,"r") as f:
	dat = [line.rstrip("\n").split() for line in f.readlines()]
results = {user : int(karma) for user, karma in dat}
del dat
user0 = choice(list(results.keys()))
users.put(user0)
userSet |= set(results.keys())

#renaming
while not users.empty():
	user = users.get()
	try:
		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		data = opener.open(baseUrl + user)
		raw_dat = data.read().decode("utf-8") 
		ind = raw_dat.find("comment-karma")
		substr = raw_dat[ind:ind+60]
		substr = substr[substr.find(">")+1:substr.find("<")]
		karma = "".join([_ for _ in substr if _.isdigit()])
		karma = int(karma)
		print( user,"\t",karma)
		results[user] = karma
		with open(outfile,"a") as f:
			f.write("%s %d\n" %(user,karma))
		new_users = re.findall("user\/(\w+)", raw_dat)
		new_users = {_ for _ in new_users if _ not in userSet}
		userSet |= new_users
		for _ in new_users:
			users.put(_)
	except:
		print( "\t\trejection...")
		sleep(5)
	#read karma here
	else:
		sleep(2)

print ("Queue emptied!")

#EOF
