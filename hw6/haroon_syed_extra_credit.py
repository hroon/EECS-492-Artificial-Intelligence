import numpy as np
import sys
import math
import scipy as sp
import copy

# classvals is a numpy size n array of class values
# class values here are Y values thresholded into quintiles
# Return the entropy of classvals
def entropy(classvals):
	# Implement this
	
	
	total = sum(classvals)
	temp = 0
	prob = classvals/total

	classes = np.count_nonzero(prob)

	for i in prob:
		temp -= i*math.log(i,classes)

	
	'''a = set()
	b = []
	for c in classvals:
		d = copy.deepcopy(a)
		a.add(c)
		if (d != a):
			b.append(c)

	nums = np.array([0,0,0,0,0])

	for c in classvals:
		for i in range(0,5):
			if (b[i] == c):
				nums[i] += 1

	print nums
	#nums = nums/float(sum(classvals))
	#print nums
	total = sum(classvals)
	print np.count_nonzero(classvals/total)


	size = len(classvals)

	e = 0
	for j in range(0,5):
		print nums[j]
		temp = nums[j]/float(size)
		print temp
		e -= ((temp)*math.log(temp,39644))

	print 

	print 'done
	'''

	return temp

# colvals is a numpy size n array of column values
# That is, a feature column with the features thresholded into quintiles
# colvals indices correspond to those in the size n classvals array
# Return expected entropy of classvals after splitting on colvals
def expected_entropy(colvals, classvals):
	# Implement this
	r1 = len(colvals)
	r2 = len(classvals)
	e = 0

	total = sum(colvals)
	temp = 0
	prob = colvals/total



	classes = r1
	for i in prob:
		#print i
		if (i <= 0.000002):
			temp += 0
		elif (i != 0):
			temp -= i*math.log(i,classes)
		else:
			temp += 0

	#P(x)*E(X) -> sum all of these up.
	for i in range(0,r1):
			e += temp*(colvals[i]/(classvals[i]))/r1


	#for i in len(classvals):
		#entropy(colvals)

	return e


if __name__ == '__main__':
	# Extract online_shares dataset
	fp = open(sys.argv[1], 'r')
	lines = fp.readlines()
	features = [st.strip() for st in lines[0].split(',')]
	features.pop() # Get rid of shares label
	data = np.genfromtxt(sys.argv[1], delimiter=',')

	X = data[1:, :data.shape[1]-1]
	Y = data[1:, data.shape[1]-1]

	# Get quintiles
	Xpercs = np.array((np.percentile(X,[20,40,60,80,100], axis=0)))
	Ypercs = np.array(np.percentile(Y,[20,40,60,80,100]))

	# Threshold everything into quintiles
	for i in range(X.shape[0]):
		for k in range(Xpercs.shape[1]):
			for j in range(Xpercs.shape[0]):
				if X[i,k] <= Xpercs[j,k]:
					X[i,k] = Xpercs[j,k]
					break

	for i in range(len(Y)):
		for j in range(len(Ypercs)):
			if Y[i] <= Ypercs[j]:
				Y[i] = Ypercs[j]
				break
	
	# Compute all information gains
	y_entropy = entropy(Y)	
	infogains = np.zeros((X.shape[1]))
	for i in range(len(infogains)):
		infogains[i] = y_entropy-expected_entropy(X[:,i],Y)

	# Sort infogains descending
	sorted_inds = np.argsort(infogains)[::-1]

	assert(len(infogains)==len(features))
	for i in range(len(sorted_inds)):
		print features[sorted_inds[i]], ',', infogains[sorted_inds[i]]


