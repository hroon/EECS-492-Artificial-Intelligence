#Haroon Syed

import sys
import utils
import copy
from collections import deque
import itertools

# Iteration limits
# Stop your search when you reach these limits
FORWARD_LIMIT = 10000
BACKWARD_LIMIT = 10000

# A useful function to get all possible n-permutations of a set of objects
# Returns an iterable generator of permutations
# Google online documentation for further reference
def getPermutations(objList, n):
	return itertools.permutations(objList, n)

'''
Tips:
Use the built-in python "set" class for set operations
	(previously in this course we used Set from the sets module,
	 but the built-in "set" works just as well if not better)
You may create your own parser and object classes if you wish,
	 as long as they are *in this file*. Using the given objects
	 in utils.py is recommended, however.
Use the getPermutations function to construct all possible action arguments,
	 so that you can initialize a list with all possible actions
'''

# *** Create whatever helper functions and classes you need in this space

class node:
	def __init__(self, inst, parent):
		self.inst = inst
		self.parent = parent

	def getInst(self):
		return self.inst

	def getParent(self):
		return self.parent

#see if precondition is entailed
# s is current set
# a is action instance
def entails(s,a):
	t = a.getPrecond()
	for element in t:
		if element not in s:
			return False
	return True

#checks to see if action is relevant
#one of actions effects must unify with an element of the goal
#action must not havny any efect that negates the goal
def back_check(s,a):
	d = a.getDelete()
	for element in d:
		if element in s:
			return False

	t = a.getAdd()
	for b in t:
		if b in s:
			return True
	return False

#takes a set and actions instance
#adds the preconditions and deletes the add list
#returns the new state
def unify(s,a):
	d = copy.deepcopy(s)
	plist = a.getPrecond()
	ulist = a.getAdd()		
	d.difference_update(ulist) #deleting the add set
	d.update(plist)	#adding pre-conditions
	return d

#takes a set and action instance
#adds the add list and deletes the delete conditions
#returns the new state
def result(s,a):
	d = copy.deepcopy(s)
	dlist = a.getDelete()
	ulist = a.getAdd()
	d.update(ulist)   #adding the addset
	d.difference_update(dlist) #getting rid of the delset
	return d

#sees if goal is in current set
#if goal is in current state, return true
def goal_test(current, goal):
	set1 = set() #current set
	set2 = set() #goal set

	for c in current:
		set1.add(str(c))
	for g in goal:
		set2.add(str(g))

	for s in set2:
		if s not in set1:
			return False
	return True

#gets successor actions
#lis is a list of actions
#count is size of list
#returns a queue of posisble states
def get_successors(current, goal, lis, count):
	cue = [] #deque()
	act = [] #deque()
	temp = None
	num = 0
	for c in range(0,count):
		if(entails(current, lis[c])):
			num += 1

	for c in range(0,count):
		if(entails(current, lis[c])):
			temp = result(current,lis[c])
			cue.append(temp)
			act1 = copy.deepcopy(lis[c])
			#act1.modParent(prev)
			act.append(act1)
			#if(goal_test(temp,goal)):
			#	return cue, True
	return cue, act


#get predecessors
def get_predecessors(current, goal, lis, count):
	cue = []
	act = []

	temp = None
	num = 0
	for c in range(0,count):
		if(back_check(current,lis[c])):
			temp = unify(current,lis[c])
			cue.append(temp)
			act1 = copy.deepcopy(lis[c])
			act.append(act1)
	return cue, act



#extract_path takes a goal node an returns a path
#list of action instances form initial state to goal state
def extract_path(current):
	#print current.getInst()
	path = []
	while current.getParent() is not None:
		#print current.getParent()
		path.append(current.getInst())
		current = current.getParent()
	path.append(current.getInst())
	path.reverse()	
	#path.pop()
	return path



# Returns true if a plan is found, along with a list of actionInst objects that forms the plan
# Returns false otherwise, with an empty list
# initial, goal, and groundObjects are sets, and actions is a list
def forward_search(initial, goal, actions, groundObjects):
	# *** Implement This Function

	current = copy.deepcopy(initial)
	pactions = [] #possible actions
	count = 0
	for a in actions:
		n = a.numargs
		perms = list(getPermutations(groundObjects, n))
		for p in perms:
			count += 1
			temp = a.getInstance(p)
			#print str(temp)
			pactions.append(temp)


	path = [] #list of actionInst objects that form path	
	queue = deque()
	closed = []

	#prev_parent = None #for extracting path
	acting = deque() #for extracting path
	node_list = []

	queue.append(current)
	acting.append(None)

	goalNode = None

	
	loop = 0
	limit =0
	if goal_test(current, goal):
		return True, path

	while len(queue) > 0 and limit < 10000:
		#print 'loop: ', loop
		loop += 1
		limit += 1
		#print 'length of queue', len(queue)
		current = queue.popleft()
		parent = acting.popleft()

		#for c in current:
		#	print str(c)
		successors, tions = get_successors(current, goal, pactions, count)
		closed.append(current)
		#for c in closed[0]:
		#	print str(c)
		for i in range(0,len(successors)):
			if goal_test(successors[i],goal):
				goalNode = node(tions[i],parent)
				path = extract_path(goalNode)
				return True, path

			if successors[i] not in queue and successors[i] not in closed:
				queue.append(successors[i])
				acting.append(node(tions[i],parent))


	return False, []

# Returns true if a plan is found, along with a list of actionInst objects that forms the plan
# Returns false otherwise, with an empty list
# initial, goal, and groundObjects are sets, and actions is a list
def backward_search(initial, goal, actions, groundObjects):
	# *** Implement this function
	current = copy.deepcopy(goal)
	goal = copy.deepcopy(initial)
	pactions = [] #possible actions
	count = 0
	for a in actions:
		n = a.numargs
		perms = list(getPermutations(groundObjects, n))
		for p in perms:
			count += 1
			temp = a.getInstance(p)
			pactions.append(temp)


	path = [] #list of actionInst objects that form path	
	queue = deque()
	closed = []
	acting = deque()
	parent = None


	queue.append(current)
	acting.append(parent)

	loop = 0
	if goal_test(goal,current):
		return True, path

	limit = 0
	while len(queue) > 0 and limit < 10000:
		#print 'loop: ', loop
		loop += 1
		limit += 1
		current = queue.popleft()
		parent = acting.popleft()
		successors, tions = get_predecessors(current, goal, pactions, count)
		closed.append(current)

		#for c in closed[0]:
		#	print str(c)
		for i in range(0,len(successors)):
			if goal_test(goal,successors[i]):
				goalNode = node(tions[i],parent)
				path = extract_path(goalNode)
				path.reverse()
				return True, path
	
			if successors[i] not in queue and successors[i] not in closed:
				queue.append(successors[i])
				#if actor is not None:
				#	print actor
				#tions[i].modParent = copy.deepcopy(actor)
				acting.append(node(tions[i],parent))

	return False, []


# Do not modify the following
if __name__=='__main__':
	assert(len(sys.argv) == 3)
	stype = sys.argv[1]
	fname = sys.argv[2]
	initial, goal, actions, groundObjects = utils.parse(fname)
	print "Actions"
	for a in actions:
		print str(a)
	print "\nInitial\n"
	for i in initial:
		print str(i)
	print "\nGoal\n"
	for g in goal:
		print str(g)
	print '\n'
	if stype == 'forward':
		foundPlan, plan = forward_search(initial, goal, actions, groundObjects)
		print foundPlan
		for a in plan:
			print str(a)
	elif stype == 'backward':
		foundPlan, plan = backward_search(initial, goal, actions, groundObjects)
		print foundPlan
		for a in plan:
			print str(a)
