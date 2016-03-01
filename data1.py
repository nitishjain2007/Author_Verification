#!/usr/bin/python
import os, sys
import random
import shutil
global author_count
global path
global value_taken
global globcount
global file_list
global yes_list
global no_list
yes_list = []
no_list = []
file_list = []
globcount = 1
value_taken = []
path = os.getcwd()
author_count = []
def get_combination(typereq):
	global author_count
	global value_taken
	if typereq == 0:
		a = random.randint(1,len(author_count))
		b = random.randint(1,author_count[a-1])
		while(1):
			while(1):
				d = random.randint(1,author_count[a-1])
				if d!=b:
					break
			possible_value1 = str(a) + "_" + str(b) + "_" + str(a) + "_" + str(d)
			possible_value2 = str(a) + "_" + str(d) + "_" + str(a) + "_" + str(b)
			if possible_value1 not in value_taken and possible_value2 not in value_taken:
				break
		value_taken.append(possible_value1)
		return possible_value1
	else:
		a = random.randint(1,len(author_count))
		while(1):
			c = random.randint(1,len(author_count))
			if a!=c:
				break
		while(1):
			b = random.randint(1,author_count[a-1])
			d = random.randint(1,author_count[c-1])
			possible_value1 = str(a) + "_" + str(b) + "_" + str(c) + "_" + str(d)
			possible_value2 = str(c) + "_" + str(d) + "_" + str(a) + "_" + str(b)
			if possible_value1 not in value_taken and possible_value2 not in value_taken:
				break
		value_taken.append(possible_value1)
		return possible_value1

def make_author_data():
	global yes_list
	global no_list
	global author_count
	global path
	authors = os.walk(path + "/Data/Authors").next()[1]
	count = 1
	author_list = path + "/Data"
	os.chdir(author_list)
	fo = open("list.txt", "wb")
	yes_list = [0]*len(authors)
	for i in range(0,len(authors)):
		temp = []
		for j in range(0,len(authors)):
			temp.append(0)
		no_list.append(temp)
	for i in authors:
		fo.write("author" + str(count) + " " + i + "\n")
		count+=1
	fo.close()
	count = 1
	for i in authors:
		currentpath = path + "/Data/Authors/" + i
		fileopen = currentpath + "/books.txt"
		lines = [line.rstrip('\n') for line in open(fileopen)]
		lines = filter(lambda a: a != "",lines)
		author_count.append(int(len(lines)/1000))
		os.mkdir(path + "/Data/Author_Data/author" + str(count))
		os.chdir(path + "/Data/Author_Data/author" + str(count))
		for j in range(0,int(len(lines)/1000)):
			data_tr = lines[j*1000:(j+1)*1000]
			length_tr = len(data_tr)
			print length_tr
			dummy = random.randint(1, length_tr-601)
			lines_to_print = data_tr[dummy:dummy+600]
			fo = open(str(j+1) + ".txt", "wb")
			for line in lines_to_print:
				fo.write(line + "\n")
			fo.close()
		count+=1

def makesame():
	global path
	global globcount
	global file_list
	global yes_list
	a = get_combination(0)
	a = a.split("_")
	source1 = path + "/Data/Author_Data/author" + a[0] + "/" + a[1] + ".txt"
	source2 = path + "/Data/Author_Data/author" + a[2] + "/" + a[3] + ".txt"
	path2 = path + "/Data/Dataset/EN" + str(globcount)
	os.mkdir(path2)
	globcount+=1
	shutil.copy2(source1, path2 + "/known01.txt")
	shutil.copy2(source2, path2 + "/unknown.txt")
	temp = ["EN" + str(globcount-1), "Y", a[0] + "_" + a[1] + "_" + a[2] + "_" + a[3]]
	file_list.append(temp)
	yes_list[int(a[0])-1]+=1

def makedifferent():
	global path
	global globcount
	global file_list
	global no_list
	a = get_combination(1)
	a = a.split("_")
	source1 = path + "/Data/Author_Data/author" + a[0] + "/" + a[1] + ".txt"
	source2 = path + "/Data/Author_Data/author" + a[2] + "/" + a[3] + ".txt"
	path2 = path + "/Data/Dataset/EN" + str(globcount)
	os.mkdir(path2)
	globcount+=1
	shutil.copy2(source1, path2 + "/known01.txt")
	shutil.copy2(source2, path2 + "/unknown.txt")
	temp = ["EN" + str(globcount-1), "N", a[0] + "_" + a[1] + "_" + a[2] + "_" + a[3]]
	file_list.append(temp)
	no_list[int(a[0])-1][int(a[2])-1]+=1
	
if __name__ == "__main__":
	global author_count
	global file_list
	global yes_list
	global no_list
	make_author_data()
	for i in range(0,10000):
		a = random.randint(0,1)
		if(a == 0):
			makedifferent()
		else:
			makesame()
	pathreq = path + "/Data/Dataset/truth.txt"
	fo = open(pathreq, "wb")
	for info in file_list:
		fo.write(info[0] + " " + info[1] + "\n")
	fo.close()
	pathreq = path + "/Data/Dataset/data_info.txt"
	fo = open(pathreq, "wb")
	for info in file_list:
		fo.write(info[0] + " " + info[2] + " " + "\n")
	fo.close()
	pathreq = path + "/Data/Dataset/yes_info.txt"
	fo = open(pathreq, "wb")
	for i in range(0,len(yes_list)):
		fo.write("author" + str(i+1) + " " + str(yes_list[i]) + "\n")
	fo.close()
	pathreq = path + "/Data/Dataset/no_info.txt"
	fo = open(pathreq, "wb")
	for i in range(0,len(yes_list)):
		for j in range(i+1,len(yes_list)):
			fo.write("author" + str(i+1) + "_" + "author" + str(j+1) + " " + str(no_list[i][j] + no_list[j][i]) + "\n")
	fo.close()
