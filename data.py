#!/usr/bin/python
import os, sys
import random
import shutil
import re
import nltk
from word_dict import dictionary
from collections import Counter
import operator
import pickle
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
global word_count
global yes_list
global no_list
global file_list
global globcount
global value_taken
global path
global author_count
word_count = {}
yes_list = []
no_list = []
file_list = []
globcount = 1
value_taken = []
path = os.getcwd()
author_count = []
chars = {
    '\xc2\x82' : ',',        # High code comma
    '\xc2\x84' : ',,',       # High code double comma
    '\xc2\x85' : '...',      # Tripple dot
    '\xc2\x88' : '^',        # High carat
    '\xc2\x91' : '\x27',     # Forward single quote
    '\xc2\x92' : '\x27',     # Reverse single quote
    '\xc2\x93' : '\x22',     # Forward double quote
    '\xc2\x94' : '\x22',     # Reverse double quote
    '\xc2\x95' : ' ',
    '\xc2\x96' : '-',        # High hyphen
    '\xc2\x97' : '--',       # Double hyphen
    '\xc2\x99' : ' ',
    '\xc2\xa0' : ' ',
    '\xc2\xa6' : '|',        # Split vertical bar
    '\xc2\xab' : '<<',       # Double less than
    '\xc2\xbb' : '>>',       # Double greater than
    '\xc2\xbc' : '1/4',      # one quarter
    '\xc2\xbd' : '1/2',      # one half
    '\xc2\xbe' : '3/4',      # three quarters
    '\xca\xbf' : '\x27',     # c-single quote
    '\xcc\xa8' : '',         # modifier - under curve
    '\xcc\xb1' : '',          # modifier - under line
    '\xc3\x80' : 'A',
    '\xc3\x81' : 'A',
    '\xc3\x82' : 'A',
    '\xc3\x83' : 'A',
    '\xc3\x84' : 'A',
    '\xc3\x85' : 'A',
    '\xc3\x86' : 'AE',
    '\xc3\x87' : 'C',
    '\xc3\x88' : 'E',
    '\xc3\x89' : 'E',
    '\xc3\x8a' : 'E',
    '\xc3\x8b' : 'E',
    '\xc3\x8c' : 'I',
    '\xc3\x8d' : 'I',
    '\xc3\x8e' : 'I',
    '\xc3\x8f' : 'I',
    '\xc3\x90' : 'D',
    '\xc3\x91' : 'N',
    '\xc3\x92' : 'O',
    '\xc3\x93' : 'O',
    '\xc3\x94' : 'O',
    '\xc3\x95' : 'O',
    '\xc3\x96' : 'O',
    '\xc3\x97' : 'x',
    '\xc3\x99' : 'U',
    '\xc3\x9a' : 'U',
    '\xc3\x9b' : 'U',
    '\xc3\x9c' : 'U',
    '\xc3\x9d' : 'Y',
    '\xc3\xa0' : 'a',
    '\xc3\xa1' : 'a',
    '\xc3\xa2' : 'a',
    '\xc3\xa3' : 'a',
    '\xc3\xa4' : 'a',
    '\xc3\xa5' : 'a',
    '\xc3\xa6' : 'ae',
    '\xc3\xa7' : 'c',
    '\xc3\xa8' : 'e',
    '\xc3\xa9' : 'e',
    '\xc3\xaa' : 'e',
    '\xc3\xab' : 'e',
    '\xc3\xac' : 'i',
    '\xc3\xad' : 'i',
    '\xc3\xae' : 'i',
    '\xc3\xaf' : 'i',
    '\xc3\xb1' : 'n',
    '\xc3\xb2' : 'o',
    '\xc3\xb3' : 'o',
    '\xc3\xb4' : 'o',
    '\xc3\xb5' : 'o',
    '\xc3\xb6' : 'o',
    '\xc3\xb9' : 'u',
    '\xc3\xba' : 'u',
    '\xc3\xbb' : 'u',
    '\xc3\xbc' : 'u',
    '\xe2\x80\x9c' : '"',
    '\xe2\x80\x9d' : '"',
    '\xe2\x80\x99' : "'",
    '\xe2\x80\x94' : "-",
    '\xe2\x80\x98' : "'"
}

def replace_chars(match):
    char = match.group(0)
    return chars[char]

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
	global word_count
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
	print authors
	for i in authors:
		print i
		currentpath = path + "/Data/Authors/" + i
		fileopen = currentpath + "/books.txt"
		lines = [line.rstrip('\n') for line in open(fileopen)]
		lines = filter(lambda a: a != "",lines)
		with open (fileopen, "r") as myfile1:
			data1 = myfile1.read()
		[extra_full1, data1]=[data1.count('!\n'), data1.replace('!\n', '!. ')]
		data1 = data1.replace('\n', ' ')
		data1 = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, data1)
		tokens1 = nltk.word_tokenize(data1)
		b = Counter(tokens1)
		req = list(set(tokens1) & set(dictionary))
		for k in req:
			if word_count.has_key(k):
				word_count[k] += b[k]
			else:
				word_count[k] = b[k]
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
		print len(list(word_count.keys()))

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
	global word_count
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
	os.chdir(path)
	print word_count
	with open("word_count.p",'wb') as f:
		pickle.dump(word_count, f)
