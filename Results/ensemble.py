import os
import collections
global classes
global author_info
global author_count
classes = [line.rstrip('\n') for line in open('lables.txt')]
author_info = [line.rstrip('\n') for line in open('data_info.txt')]
author_info = [x.split(" ")[1] for x in author_info]
author_info = [[int(x.split("_")[0]), int(x.split("_")[2])] for x in author_info]
author_count = {}
yes_instances = [line.rstrip('\n') for line in open('yes_info.txt')]
no_instances = [line.rstrip('\n') for line in open('no_info.txt')]
for j in range(0,len(yes_instances)):
	author_count[str(j+1) + "_" + str(j+1)] = int(yes_instances[j].split(" ")[1])
temp=0
for i in range(0,16):
	for j in range(i+1,16):
		author_count[str(i+1) + "_" + str(j+1)] = int(no_instances[temp].split(" ")[1])
		temp+=1		

def calculate_5_fold():
	global classes
	global author_info
	global author_count
	errors = {}
	accu = []
	nn_accu = []
	tree_bagger_accu = []
	random_forest_accu = []
	rbf_svm_accu = []
	naive_bayes_accu = []
	for i in range(0,16):
		for j in range(i,16):
			errors[str(i+1) + "_" + str(j+1)] = 0	
	for i in range(0,5):
		nn = [line.rstrip('\n') for line in open('NN/5_fold/'+str(i+1) + ".txt")]
		treebagger = [line.rstrip('\n') for line in open('treebagger/5_fold/'+str(i+1) + ".txt")]
		random_forest = [line.rstrip('\n') for line in open('random_forest/5_fold/'+str(i+1) + ".txt")]
		rbf_svm = [line.rstrip('\n') for line in open('RBF_SVM/5_fold/'+str(i+1) + ".txt")]
		naive_bayes = [line.rstrip('\n') for line in open('Naive_Bayes/5_fold/'+str(i+1) + ".txt")]
		classes_req = classes[i*len(nn):(i+1)*len(nn)]
		ans = []
		for k in range(0,len(nn)):
			temp = [nn[k],random_forest[k],rbf_svm[k]]
			ans.append(temp)
		ans = [collections.Counter(x).most_common()[0][0] for x in ans]
		count = 0
		nn_count = 0
		treebagger_count = 0
		random_forest_count = 0
		rbf_svm_count = 0
		naive_bayes_count = 0
		#print "for ensemble"
		for j in range(0,len(ans)):
			if ans[j] == classes_req[j]:
				count = count + 1
			else:
				try:
					errors[str(author_info[i*len(nn)+j][0]) + "_" + str(author_info[i*len(nn)+j][1])] += 1
				except KeyError:
					errors[str(author_info[i*len(nn)+j][1]) + "_" + str(author_info[i*len(nn)+j][0])] += 1
			if nn[j] == classes_req[j]:
				nn_count = nn_count + 1
			if treebagger[j] == classes_req[j]:
				treebagger_count = treebagger_count + 1
			if random_forest[j] == classes_req[j]:
				random_forest_count = random_forest_count + 1
			if rbf_svm[j] == classes_req[j]:
				rbf_svm_count = rbf_svm_count + 1
		print float(float(count)/float(len(nn)))*100
		accu.append(float(float(count)/float(len(nn)))*100)
		nn_accu.append(float(float(nn_count)/float(len(nn)))*100)
		tree_bagger_accu.append(float(float(treebagger_count)/float(len(nn)))*100)
		random_forest_accu.append(float(float(random_forest_count)/float(len(nn)))*100)
		rbf_svm_accu.append(float(float(rbf_svm_count)/float(len(nn)))*100)
		'''count = 0
		print "for nn"
		for j in range(0,len(nn)):
			if nn[j] == classes_req[j]:
				count = count + 1
		print float(float(count)/float(len(nn)))*100
		count = 0
		print "for tree_bagger"
		for j in range(0,len(treebagger)):
			if treebagger[j] == classes_req[j]:
				count = count + 1
		print float(float(count)/float(len(treebagger)))*100
		count = 0
		print "for random_forest"
		for j in range(0,len(random_forest)):
			if random_forest[j] == classes_req[j]:
				count = count + 1
		print float(float(count)/float(len(random_forest)))*100'''
	print "printing errors"
	for i in range(0,16):
		for j in range(i,16):
			print "for " + str(i+1) + " and " + str(j+1) + " is " + str(float(errors[str(i+1) + "_" + str(j+1)])/float(author_count[str(i+1) + "_" + str(j+1)])*100)
	print "mean is ", sum(accu) / float(len(accu))
	print "mean for nn is ", sum(nn_accu) / float(len(nn_accu))
	print "mean for tree_bagger is ", sum(tree_bagger_accu) / float(len(tree_bagger_accu))
	print "mean for random_forest is ", sum(random_forest_accu) / float(len(random_forest_accu))
	print "mean for rbf_svm is ", sum(rbf_svm_accu) / float(len(rbf_svm_accu))

def calculate_10_fold():
	global classes
	accu = []
	nn_accu = []
	tree_bagger_accu = []
	random_forest_accu = []
	rbf_svm_accu = []
	naive_bayes_accu = []
	for i in range(0,10):
		nn = [line.rstrip('\n') for line in open('NN/10_fold/'+str(i+1) + ".txt")]
		treebagger = [line.rstrip('\n') for line in open('treebagger/10_fold/'+str(i+1) + ".txt")]
		random_forest = [line.rstrip('\n') for line in open('random_forest/10_fold/'+str(i+1) + ".txt")]
		rbf_svm = [line.rstrip('\n') for line in open('RBF_SVM/10_fold/'+str(i+1) + ".txt")]
		naive_bayes = [line.rstrip('\n') for line in open('Naive_Bayes/10_fold/'+str(i+1) + ".txt")]
		classes_req = classes[i*len(nn):(i+1)*len(nn)]
		ans = []
		for i in range(0,len(nn)):
			temp = [nn[i],random_forest[i],rbf_svm[i]]
			ans.append(temp)
		ans = [collections.Counter(x).most_common()[0][0] for x in ans]
		count = 0
		nn_count = 0
		treebagger_count = 0
		random_forest_count = 0
		rbf_svm_count = 0
		naive_bayes_count = 0
		for j in range(0,len(ans)):
			if ans[j] == classes_req[j]:
				count = count + 1
			if nn[j] == classes_req[j]:
				nn_count = nn_count + 1
			if treebagger[j] == classes_req[j]:
				treebagger_count = treebagger_count + 1
			if random_forest[j] == classes_req[j]:
				random_forest_count = random_forest_count + 1
			if rbf_svm[j] == classes_req[j]:
				rbf_svm_count = rbf_svm_count + 1
		print float(float(count)/float(len(nn)))*100
		accu.append(float(float(count)/float(len(nn)))*100)
		nn_accu.append(float(float(nn_count)/float(len(nn)))*100)
		tree_bagger_accu.append(float(float(treebagger_count)/float(len(nn)))*100)
		random_forest_accu.append(float(float(random_forest_count)/float(len(nn)))*100)
		rbf_svm_accu.append(float(float(rbf_svm_count)/float(len(nn)))*100)
	print "mean is ", sum(accu) / float(len(accu))
	print "mean for nn is ", sum(nn_accu) / float(len(nn_accu))
	print "mean for tree_bagger is ", sum(tree_bagger_accu) / float(len(tree_bagger_accu))
	print "mean for random_forest is ", sum(random_forest_accu) / float(len(random_forest_accu))
	print "mean for rbf_svm is ", sum(rbf_svm_accu) / float(len(rbf_svm_accu))
				
if __name__=="__main__":
	calculate_5_fold()
	print "\n"
	calculate_10_fold()
