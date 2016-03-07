from __future__ import division
import itertools
from collections import OrderedDict
from operator import itemgetter

# ---------------------- Footprint cases retrieval -----------------------


















fp = open('input.txt')
inp = fp.readlines() #.rstrip()
data = [word.strip() for word in inp]
#print data

#------------ Coverage of a reference ----------------

cov = {}
for d in data:
	temp = d.split(':')
	cov[temp[0]] = temp[1]
	
#print 'Coverage',cov

#---------------- Reverse map of a reference ------------

Rv = {}
for d in data:
	temp = d.split(':')
        temp2 = temp[1].split(',')
        for t in temp2:
                #print t
                if Rv.has_key(t):
        		res = Rv.get(t)
        		res.append(temp[0])
        		Rv[t] = res
        	else:
        	        res = []
        		res.append(temp[0])
        		Rv[t] = res
        		
#print 'Reachability',Re

#-----------Rechability of a reference -----------

Re = {}
for key,value in cov.items():
	lis = cov.get(key)
	lis = lis.split(',')
	temp = []
	for l in lis:
		temp.append(Rv.get(l))
	#print key
	#print temp
	merged = list(itertools.chain(*temp))
	res = list(set(merged))
	Re[key] = res

#print 'Reachability',Re

#----------- Relative coverage of a reference ------

RC = {}
for key,value in Re.items():
	value = Re.get(key)
	rc = len(value) - 1
	if rc == 0:
		rc = 999999
		RC[key] = rc
	else:
		RC[key] = 1/rc

d = OrderedDict(sorted(RC.items(), key=itemgetter(1), reverse = True))
# OrderedDict preserves the order we give
print 'Relative coverage', d





