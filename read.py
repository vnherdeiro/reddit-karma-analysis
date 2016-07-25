#! /usr/bin/python

import matplotlib.pylab as plt
from sys import argv
import pickle
from collections import Counter
from scipy.optimize import curve_fit
from operator import itemgetter #used to sort according to the values field
import numpy as N
from scipy.constants import golden

def func(var,exp,amp):
	return amp*var**exp

infile = argv[1]

#with open(infile,"r") as f:
#	dat = pickle.load(f)

with open(infile,"r") as f:
	dat = [line.rstrip("\n").split() for line in f.readlines()]
dat = {user:int(karma) for user, karma in dat}

print "Top 10"
for order, (user, karma) in enumerate(sorted(dat.items(),key=itemgetter(1),reverse=1)[:10]):
	print "\t\t",order+1,"\t",user,"\t\t\t",karma

print "Stats:", len(dat)
occurences = Counter(dat.values())
x, y = map(N.array,zip(*occurences.items()))
cut = (x>0)#&(x<10000)
x, y = x[cut], y[cut]
y = y.astype(N.float64)
y /= N.sum(y)
fp, fc = curve_fit(func,x,y)
print "\tPower Law fit:\t",fp[0],"+/-",N.sqrt(fc[0][0])

wSize = 10.
plt.figure(figsize=(wSize,wSize/golden))
plt.scatter(x,y,c="#80001c",lw=0)
plt.plot(x,func(x,*fp),c=".5",lw=1.5)
plt.xscale("log")
plt.yscale("log")
plt.xlim([1,x.max()])
plt.grid()
plt.tight_layout()
plt.show()

#EOF
