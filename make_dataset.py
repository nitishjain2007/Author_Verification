#!/usr/bin/python
import os, sys
import random
import shutil
global path  
path = os.getcwd()
global count 
count = 0
global taken 
taken = []
global fileinfo 
fileinfo = []

def get_combination(value):
	global count
	global taken
	global path
	if value == 1:
		while(1):
			a = random.randint(1,8)
			while(1):
				b = random.randint(1,8)
				if (b!=a):
					break
			c = random.randint(1,50)
			d = random.randint(1,50)
			temp = [str(a) + "." + str(c), str(b) + "." + str(d)]
			if temp not in taken:
				taken.append(temp)
				taken.append(temp[::-1])
				break
		return temp
	else:
		while(1):
			a = random.randint(1,8)
			c = random.randint(1,50)
			d = random.randint(1,50)
			temp = [str(a) + "." + str(c), str(a) + "." + str(d)]
			if temp not in taken:
				taken.append(temp)
				taken.append(temp[::-1])
				break
		return temp

def makedifferent():
	global count
	global fileinfo
	global path
	comb = get_combination(1)
	first = comb[0]
	second = comb[1]
	source1 = path + "/authors/author" + first.split('.')[0] + "/data/" + first.split('.')[1] + ".txt"
	source2 = path + "/authors/author" + second.split('.')[0] + "/data/" + second.split('.')[1] + ".txt"
	path2 = path + "/gutenberg/EN" + str(count)
	os.mkdir(path2)
	count+=1
	shutil.copy2(source1, path2 + "/known01.txt")
	shutil.copy2(source2, path2 + "/unknown.txt")
	temp = ["EN"+str(count-1),"N"]
	fileinfo.append(temp)

def makesame():
	global count
	global fileinfo
	global path
	comb = get_combination(0)
	first = comb[0]
	second = comb[1]
	source1 = path + "/authors/author" + first.split('.')[0] + "/data/" + first.split('.')[1] + ".txt"
	source2 = path + "/authors/author" + second.split('.')[0] + "/data/" + second.split('.')[1] + ".txt"
	path2 = path + "/gutenberg/EN" + str(count)
	os.mkdir(path2)
	count+=1
	shutil.copy2(source1, path2 + "/known01.txt")
	shutil.copy2(source2, path2 + "/unknown.txt")
	temp = ["EN"+str(count-1),"Y"]
	fileinfo.append(temp)

if __name__=="__main__":
	global count
	global fileinfo
	global taken
	global path
	for i in range(0,1000):
		a = random.randint(0,1)
		if(a == 0):
			makedifferent()
		else:
			makesame()
	pathreq = path + "/gutenberg/truth.txt"
	fo = open(pathreq, "wb")
	for info in fileinfo:
		fo.write(info[0] + " " + info[1] + "\n")
	fo.close()