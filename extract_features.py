import re
import nltk
from collections import Counter
import numpy
import operator
import pickle
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
global word_count
word_count = pickle.load(open("word_count.p", "rb"))
global word_count_sorted
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

def rare_words(tokens1, tokens2):
	global word_count_sorted
	rare = 	word_count_sorted[0:15100]
	rare1 = list(set(tokens1) & set(rare))
	rare2 = list(set(tokens2) & set(rare))
	rare1_no = Counter(tokens1)
	rare2_no = Counter(tokens2)
	rare1_total = sum([rare1_no[x] for x in rare1])
	rare2_total = sum([rare2_no[x] for x in rare2])
	rare1_count = float(rare1_total)/float(len(tokens1))
	rare2_count = float(rare2_total)/float(len(tokens2))
	if rare1_count < rare2_count:
		return rare1_count/rare2_count
	else:
		return rare2_count/rare1_count

def function_words(tokens1, tokens2):
	global word_count_sorted
	function_list = word_count_sorted[-100:]
	function1 = list(set(tokens1) & set(function_list))
	function2 = list(set(tokens2) & set(function_list))
	function1_no = Counter(tokens1)
	function2_no = Counter(tokens2)
	function1_total = sum([function1_no[x] for x in function1])
	function2_total = sum([function2_no[x] for x in function2])
	function1_count = float(function1_total)/float(len(tokens1))
	function2_count = float(function2_total)/float(len(tokens2))
	if function1_count < function2_count:
		return function1_count/function2_count
	else:
		return function2_count/function1_count

def punc_func(tokens1,tokens2,extra_full1,extra_full2):
	punc =['.',',','/','-','?','!',';',':']
	punc_count_personal1 = [tokens1.count(x) for x in punc]
	punc_count_personal2 = [tokens2.count(x) for x in punc]
	punc_count_personal1[0]-=extra_full1
	punc_count_personal2[0]-=extra_full2
	count1 = sum(punc_count_personal1)
	count2 = sum(punc_count_personal2)
	punc_count_personal1 = [int((float(i)/count1)*(10**12)) for i in punc_count_personal1]
	punc_count_personal2 = [int((float(i)/count2)*(10**12)) for i in punc_count_personal2]
	return [[punc_count_personal1, punc_count_personal2],[count1,count2]]

def sen_length(tokens1, tokens2, extra_full1, extra_full2):
	split=['.','?']#'!']#,';']
	punc =['.',',','?','!',';',':']
	[w1,s1,current_sen_count,short_sen1,long_sen1]=[0,0,0,0,0];
	for i in tokens1:
		current_sen_count+=1
		if i in split:
			s1+=1
			temp=current_sen_count - 1
			current_sen_count = 0
			if temp<=6:
				short_sen1+=1
			if temp>=12:
				long_sen1+=1
		if not (i in punc):
			w1+=1
	av1=float(w1)/s1
	[w2,s2,current_sen_count,short_sen2,long_sen2]=[0,0,0,0,0];
	for i in tokens2:
		current_sen_count+=1
		if i in split:
			s2+=1
			temp=current_sen_count - 1
			current_sen_count = 0
			if temp<=6:
				short_sen2+=1
			if temp>=12:
				long_sen2+=1
		if not i in punc:
			w2+=1
	av2=float(w2)/s2
	return [[av1,av2],[[(short_sen1*1.0)/s1,(long_sen1*1.0)/s1],[(short_sen2*1.0)/s2,(long_sen2*1.0)/s2]]]

def unique(tokens1, tokens2):
	punc =['.',',','?','!',';',':']
	#for i in punc
	tokens1= [j for j in tokens1 if j not in punc]
	tokens2= [j for j in tokens2 if j not in punc]
	u1=float(len(set(tokens1)))/len(tokens1)
	u2=float(len(set(tokens2)))/len(tokens2)
	return abs(u1-u2)

def sen_list(tagged1,tagged2):
	punc =['.','?',';']
	sen_list1=[]
	sen_list2=[]
	sen=[]
	for i in tagged1:
		if not i[0] in punc:
			sen.append(i)
		else:
			sen_list1.append(sen)
			sen=[]
	for i in tagged2:
		if not i[0] in punc:
			sen.append(i)
		else:
			sen_list2.append(sen)
			sen=[]
	return [sen_list1,sen_list2]

def overlap(known,unknown):
	[A,B]=[zip(known, known[1:]),zip(unknown, unknown[1:])]
 	bi_overlap=set(A).intersection(set(B)).__len__()
	[A,B]=[zip(known, known[1:], known[2:]),zip(unknown, unknown[1:], unknown[2:])]
	tri_overlap=set(A).intersection(set(B)).__len__()
	return [bi_overlap,tri_overlap]

def POS_overlap(kt,ut):
	[k,u]=[list(zip(*kt)[1]),list(zip(*ut)[1])]
	[A,B]=[zip(k, k[1:]),zip(u,u[1:])]
 	return set(A).intersection(set(B)).__len__()
	#[k,u]=sen_list(known,unknown)
	#[nltk.pos_tag(i) for i in k]	

def POS_start(kt,ut):
	[ktlines,utlines]=sen_list(kt,ut)
	while [] in ktlines:
		ktlines.remove([])
	while [] in utlines:
		utlines.remove([])
	kstart=[zip(*i)[1][0] for i in ktlines]
	ustart=[zip(*i)[1][0] for i in utlines]
	k=Counter(kstart)
	k=sorted(k.items(), key=operator.itemgetter(1),reverse=True)
	u=Counter(ustart)
	u=sorted(u.items(), key=operator.itemgetter(1),reverse=True)
	#in first k=3 
	return len(set(zip(*k[0:3])[0]).intersection(zip(*u[0:3])[0]))	

def POS_freq(kt,ut):
	[ktlines,utlines]=sen_list(kt,ut)
	k=zip(*kt)[1] #tags in order 
	u=zip(*ut)[1]
	k=Counter(k)	#tags in decreasing freq order
	u=Counter(u)
	k=sorted(k.items(), key=operator.itemgetter(1),reverse=True)
	u=sorted(u.items(), key=operator.itemgetter(1),reverse=True)
	return len(set(zip(*k[0:5])[0]).intersection(zip(*u[0:5])[0]))

def ret_feature(directory):
	with open (directory+"/known01.txt", "r") as myfile1:
		data1 = myfile1.read()
	with open (directory+"/unknown.txt", "r") as myfile2:
		data2 = myfile2.read()
	feature=[0]*12
	[extra_full1, data1]=[data1.count('!\n'), data1.replace('!\n', '!. ')]
	[extra_full2, data2]=[data2.count('!\n'), data2.replace('!\n', '!. ')]
	data1 = data1.replace('\n', ' ')
	data2 = data2.replace('\n', ' ')
	data1 = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, data1)
	data2 = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, data2)
	tokens1 = nltk.word_tokenize(data1)
	tokens2 = nltk.word_tokenize(data2)
	tagged1 = nltk.pos_tag(tokens1)
	tagged2 = nltk.pos_tag(tokens2)
	[[punc_count_personal1, punc_count_personal2],[count1,count2]]=punc_func(tokens1,tokens2,extra_full1,extra_full2)
	feature[0]= rare_words(tokens1,tokens2)	
	feature[1]= abs(count1*1.0/len(tokens1) - count2*1.0/len(tokens2)) 
	t=((numpy.array(punc_count_personal1)) - 1.0*(numpy.array(punc_count_personal2)))/10**12
	feature[2]=abs(t).mean()
	[[av1,av2],[vec1,vec2]]=sen_length(tokens1, tokens2, extra_full1, extra_full2)
	t=numpy.array(vec1)-numpy.array(vec2)
	t=abs(t)	
	feature[3]=t.mean()
	feature[4]=abs(av1-av2)
	feature[5]=unique(tokens1, tokens2)
	[a,b]=overlap(tokens1,tokens2)
	feature[6]=a
	feature[7]=b
	feature[8]=POS_freq(tagged1,tagged2)
	feature[9]=POS_overlap(tagged1,tagged2)
	feature[10]=POS_start(tagged1,tagged2)
	feature[11]=function_words(tokens1, tokens2)
	return feature


if __name__=="__main__":
	global word_count
	global word_count_sorted
	word_count_sorted = [x[0] for x in sorted(word_count.items(), key=operator.itemgetter(1))]
	lines = [line.rstrip('\n') for line in open('truth.txt')]
	a=[]
	for line in lines:
		a.append(line.split(' '))
	dirs=list(zip(*a)[0])
	classes=list(zip(*a)[1])
	x = {'N':0 ,'Y':1}
	classes=[x[i] for i in classes]
	
	point_list=[]
	for i in dirs:
		point_list.append(ret_feature(i))
		print i
	thefile=open('lables.txt','w')

	f2=open('data.txt','w')

	
	for i in classes:
		thefile.write("%s\n" % i)
	for i in point_list:
		for j in i:
			f2.write("%s " % j)
		f2.write("\n")
