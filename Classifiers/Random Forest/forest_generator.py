import os
import sys
import random
from scipy.stats import mode
from tree_generator import DecisionTree


class Forest(object):

	""" A Class used for implemnting the forest of the random forest algorithm"""
	
	def __init__(self, height=10, fraction=0.5, treescount=20):
		self.height = height
		self.fraction = fraction
		self.treescount = treescount
		self.trees = []

	def makeforest(self,Data,Classes):
		numberofsamples = int(len(Classes)*0.8) # numberofsamples = fraction of samples to be trained * total nno of points in training
		for i in xrange(self.treescount):
			#print "Constructiong tree " + str(i)
			indicesreq = random.sample(xrange(len(Classes)),numberofsamples)
			data_new = [Data[i] for i in indicesreq]
			classes_new = [Classes[i] for i in indicesreq]
			new_tree = DecisionTree(self.height,self.fraction)
			new_tree.make_tree(data_new,classes_new)
			self.trees.append(new_tree)

	def give_result(self, Data):
		sample_size = len(Data)
		forest_size = len(self.trees)
		predictions = []
		for i in xrange(forest_size):
			predictions.append(self.trees[i].predict(Data))
		return mode(predictions)[0][0]

	def accuracy(self,Data,Classes):
		predictions = self.give_result(Data)
		sample_size = len(Classes)
		count = 0
		for i in xrange(sample_size):
			yc=0
			nc=0
			if(predictions[i]==Classes[i]):
				count += 1
		#print list(predictions).count(1)*1.0/len(predictions)
		print str(count)+'/'+str(sample_size)
		success = (float(count)/float(sample_size))*100
		return [predictions,success]
