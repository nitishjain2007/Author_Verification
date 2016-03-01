from forest_generator import Forest
#from sklearn import datasets
import os
#import matplotlib.pyplot as plot
import sys

if __name__ == "__main__":
	data = []
	classes = []
	lines = [line.rstrip('\n') for line in open('../../Data/Dataset/data.txt')]
	for line in lines:
		data.append(map(float, line.split(' ')[:-1]))
	lines = [line.rstrip('\n') for line in open('../../Data/Dataset/lables.txt')]
	classes = map(int, lines)
	n = raw_input("Select n for n-fold: ")
	n = int(n)
	#print data
	#print classes
	maxi = []
	for i in range(0,n):
		h = len(data)
		h = h/n
		data1 = data[:i*h] + data[(i+1)*h:]
		classes1 = classes[:i*h] + classes[(i+1)*h:]
		data2 = data[i*h:(i+1)*h]
		classes2 = classes[i*h:(i+1)*h]
		random_forest = Forest(31,0.5,39)
		random_forest.makeforest(data1, classes1)
		ans = random_forest.accuracy(data2, classes2)
		maxi.append(ans[1])
		fo = open(str(i) + ".txt", "wb")
		for j in ans[0]:
			fo.write(str(j) + "\n")
		fo.close()
		print ans[1]
	print maxi
	print "max is ", max(maxi)
	print "index is ", maxi.index(max(maxi))
'''plot.plot(range(51,996),maxi)
plot.show()
target = open('results.txt', 'wb')
for i in maxi:
	target.write(str(i) + "\n")
target.close()'''
