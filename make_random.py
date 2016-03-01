import os, sys
import random
import shutil
import sys
reload(sys)
path = os.getcwd()
data_file = path + "/Data/Dataset/data.txt"
label_file = path + "/Data/Dataset/lables.txt"
data = [line.rstrip('\n') for line in open(data_file)]
labels = [line.rstrip('\n') for line in open(label_file)]
os.mkdir(path + "/Data/Dataset/RandomDataset")
for i in range(0,len(data)):
	data[i] = data[i] + str(i+1)
for j in range(0,200):
	os.mkdir(path + "/Data/Dataset/RandomDataset/set" + str(j+1))
	os.chdir(path + "/Data/Dataset/RandomDataset/set" + str(j+1))
	random.shuffle(data)
	fo = open("data.txt", "wb")
	for line in data:
		data_p = line.split(" ")
		for i in data_p[0:-1]:
			fo.write(i + " ")
		fo.write("\n")
	fo.close()
	fo = open("lables.txt", "wb")
	count=0
	for line in data:
		data_p = line.split(" ")
		fo.write(labels[int(data_p[-1])-1] + "\n")
	fo.close()
	fo = open("mapping.txt", "wb")
	for line in data:
		data_p = line.split(" ")
		fo.write(data_p[-1] + "\n")
	fo.close()
