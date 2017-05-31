from sets import Set
from collections import deque
import heapq
from copy import copy,deepcopy
# A class that wraps the heapq functionality
# into a convenient min heap container
# which always maintains the smallest element of
# a set of data, with O(log(n)) insertion and removal
# This heap does not support node cost updating, so just
# insert duplicate nodes with different path costs if necessary
class MinHeap:
	def __init__(self):
		self.container = []
	
	def push(self, obj):
		heapq.heappush(self.container, obj)

	def pop(self):
		return heapq.heappop(self.container)

	def top(self):
		return self.container[0]
	
	# So that you can call the python len() function on this object
	def __len__(self):
		return len(self.container)

# An implementation of the node class
# You may re-implement this if you wish
# But then be sure to re-implement the extract_path function
class node:
	node_count = 0
	def __init__(self, parent, position, pathcost=0, heuristic=0):
		self.idnum = node.node_count
		node.node_count += 1
		self.position = position
		self.pathcost = pathcost
		self.heuristic = heuristic
		self.totalcost = pathcost+heuristic
		self.parent = parent
		if parent is None:
			self.depth = 0
		else:
			self.depth = parent.depth+1

	# Less-than implemented so nodes can be put in MinHeap
	def __lt__(self, other):
		return self.totalcost < other.totalcost

	# Equality implemented so you can test whether nodes
	# are in a Set()
	# Nodes are equivalent if their positions are equal
	def __eq__(self, other):
		return (self.position == other.position)

	# Hash implemented so nodes can be put in Set()
	def __hash__(self):
		return hash(self.position)
	def print_node(self):
		print "idnum: ", self.idnum
		print "position: ", self.position
		print "pathcost: ", self.pathcost
		print "parent: ", self.parent
		print "depth: ", self.depth
		print "totalcost ", self.totalcost

# A dummy heuristic function that always returns 0
# Useful for searches that don't have a heuristic
def zero_heuristic(curpos, endpos):
	return 0

# Manhattan distance between curpos and endpos (tuples)
def manhattan(curpos, endpos):
	return abs(endpos[0]-curpos[0])+abs(endpos[1]-curpos[1])

# Euclidean distance between curpos and endpos (tuples)
def euclidean(curpos, endpos):
	return ((curpos[0]-endpos[0])**2+(curpos[1]-endpos[1])**2)**(0.5)


#makes sure the position is on the grid
def check(position, grid):
	x = position[0]
	y = position[1]
	a = True 
	try:					#Throw an error if we go off the grid
		grid[x][y]
	except(IndexError): 
		a = False
	if(a == True):
		if(x < 0 or y < 0):
			return False
		if(grid[x][y] != 0):
			return True
	return False

#function that takes the current node, the grid and goal
# and returns successors for uniform cost search
#checks at generation
def generation(curnode,grid,endpos,sat,heurisitic = zero_heuristic):
	position = curnode.position
	x = position[0]
	y = position[1]

	north = (x-1, y)
	east = (x, y+1)
	south = (x+1, y)
	west = (x, y-1)
	successors = []				#initializing successors list
	pos = Set()				#putting successor locations in a Set
	size = 0					#the size of the successors list
	goal = False
	final = None

	if (check(north,grid)):
			if(north not in sat ):
				n = node(curnode, north, 1, 0)
				successors.append(n)			#add succesors to list
				pos.add(north)						#add position to set
				size += 1	
				#print 'north'
				#if(north == endpos):			#if goal, make goal found
					#goal = True					#it still will add the other nodes to
					#final = n                   #list, so thats why my node count might be high
					#return(successors, pos,size)
	if (check(east,grid)):
			if(east not in sat):
				e = node(curnode, east, 2, 0)
				successors.append(e)
				pos.add(east)
				size += 1
				#print 'east'
				#if(east == endpos):
					#goal = True
					#successors = []
					#successors.append(e)
					#return(successors, pos,size)
					#final = e
	if (check(south,grid)):
			if(south not in sat):
				s = node(curnode, south, 3, 0)
				successors.append(s)
				pos.add(south)
				size += 1
				#print 'south'
				#if(south == endpos):
				#	goal = True
					#successors = []
					#successors.append(s)
					#return(successors, pos,size)
					#final = s
	if (check(west,grid)):
			if(west not in sat):
				w = node(curnode, west, 4, 0)
				successors.append(w)
				pos.add(west)
				size += 1
				#print 'west'
				#if(west == endpos):
					#goal = True
					#successors = []
					#successors.append(w)
					#final = w
					#return(successors, pos,size)
	#print pos
	return (successors,pos,size,goal,final)
	#returns the successor list, the position set, set size, and whether it found goal

# A function that takes the current node, the grid,
# The goal position (endpos), and possibly the heuristic function, and returns a list of successors
# Different from the function above, as this one tests at expansion
# Almost identical to generation, but this one does not goal test 
def get_successors(curnode, grid, endpos, sat, heuristic):
	# Fill in this function
	# You may want to create several versions of this function
	# Insert successors in the order north, east, south, west
	position = curnode.position
	x = position[0] #row
	y = position[1] #column

	north = (x-1, y)
	east = (x, y+1)
	south = (x+1, y)
	west = (x, y-1)
	successors = []
	pos = Set()
	size = 0
	goal = False
	cos = 0
	#print curnode.position
	##### Your code here ######
	if (check(north,grid)):
			if(north not in sat ):
				cos = heuristic(north,endpos)
				n = node(curnode, north, 1, cos)
				successors.append(n)
				pos.add(north)
				#pos.add(n)
				size += 1
				#if(north == endpos):
				#	goal = True
				#	return(successors, pos,size)
	if (check(east,grid)):
			if(east not in sat):
				cos = heuristic(east,endpos)
				e = node(curnode, east, 2, cos)
				successors.append(e)
				pos.add(east)
				#pos.add(e)
				size += 1
				#if(east == endpos):
				#	goal = True
				#	successors = []
				#	successors.append(e)
				#	return(successors, pos,size)
	if (check(south,grid)):
			if(south not in sat):
				cos = heuristic(south,endpos)
				s = node(curnode, south, 3, cos)
				successors.append(s)
				pos.add(south)
				#pos.add(e)
				size += 1
				#if(south == endpos):
				#	goal = True
				#	successors = []
				#	successors.append(s)
				#	return(successors, pos,size)
	if (check(west,grid)):
			if(west not in sat):
				cos = heuristic(west,endpos)
				w = node(curnode, west, 4, cos)
				successors.append(w)
				pos.add(west)
				#poss.add(w)
				size += 1
				#if(west == endpos):
				#	goal = True
				#	successors = []
				#	successors.append(w)
				#return(successors, pos,size)
	#print pos
	return (successors,pos,size)

# A function that tests whether a node is a goal node
def goal_test(curnode, endpos):
	return (curnode.position == endpos)

# extract_path takes a goal node and returns a path
# (a list of tuples) from the initial state to the goal.
# If you change the node class, re-implement this function
def extract_path(curnode):
	path = []
	while curnode is not None:
		path.append(curnode.position)
		curnode = curnode.parent
	return path[::-1]

#extract cost takes a goal node and returns total cost
def extract_cost(curnode):
	#path = []
	cost = 0
	while curnode is not None:
		try: 
			cost += curnode.pathcost
		except(AttributeError):
			return cost
		#print cost
		curnode = curnode.parent
	return cost

#checks to see if container is empty
#returns true if its empty
def isempty(d):
	if d:
		return False
	return True


# For all of the following search functions,
# "grid" is a python list of lists of integers describing the board
# Index the grid via grid[rowindex][columnindex]
# startpos is a tuple of the agent's starting position
# endpos is the location of the batter
# Do not change the arguments or return values of these functions
def depth_first_search(grid, startpos, endpos):
	# Perform depth-first search
	# Goal test at generation
	#ef __init__(self, parent, position, pathcost=0, heuristic=0):
	current = node( None, startpos, 0, 0)
	tn = 1 #total_nodes_generated
	c_max = 0 #current_nodes_stored
	mmax = 0 #max number of nodes stored
	iters = 0 #num_iterations
	deck = deque() 
	frontier = Set()	#stores locations added to frontier
	explored = Set()	#stores locations already explored
	fro = Set()
	#while(goal_test(current, endpos) == False):
	print 'start'
	frontier.add(current)
	fro.add(current.position)
	goal = False
	while(goal == False):
		#print 'explored: ',explored
		#if iters == 5:
		#	return ''
		start = True
		#print 'current: ', current.position
		
		frontier.remove(current)
		fro.remove(current.position)
		explored.add(current.position) #adding current location to explored set
		suc = generation(current,grid,endpos,explored,0) #gets list of successors
		p_successors = suc[0] #possible successors
		p_size = 0;

		for i in range(0,suc[2]):
			if (p_successors[i] not in frontier): #if successors isn't in the frontier
				nex = p_successors[i]
				#print nex.position
				deck.append(nex) #add it to the frontier
				frontier.add(nex)
				fro.add(nex.position)
				p_size += 1
				if(goal_test(nex,endpos) == True):
					cost = extract_cost(nex)
					goal = True
					tn += p_size
					c_max = len(deck)
					if(mmax < c_max):
						mmax = c_max
						c_max = c_max - 1
					iters += 1
					return nex, tn, mmax, iters, nex.depth, cost
		tn += p_size
		#print 'frontier: ',fro
		#print 'explored: ',explored
		c_max = len(deck)
		#frontier.remove(current)
		#fro.remove(current.position)
		current = deck.pop()
		frontier.add(current)
		fro.add(current.position)
		if(mmax < c_max):
			mmax = c_max
		c_max = c_max - 1
		iters += 1
		#if(suc[3] == True):
			#current = suc[4]
	# Return all of the following, in order
	#cost = 0
	#cost = extract_cost(current)
	#return current, tn, mmax, iters, current.depth, cost
	#goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal

def iterative_deepening_search(grid, startpos, endpos):
	# Perform iterative deepening search
	# Goal test at generation
	d = 10000; #depth
	tn = 1 #total nodes generated
	mmax = 0 #max_number of nodes stored
	iters = 0 #number of iterations
	for i in range(0,d): #gets deeper with every loop
		#current = node(None, startpos, 0, 0)
		deck = deque()
		brk = False 
		frontier = Set() 
		explored = Set() #explored locations
		current = node(None, startpos, 0, 0)
		frontier.add(current)
		#print 'depth',i
		while(brk == False): #while depth is low;
			frontier.remove(current)
			cur_depth = current.depth
			#print 'current',current.position, current.depth
			explored.add(current.position)
			suc = generation(current,grid,endpos,explored,0)
			p_successors = suc[0]
			p_size = 0;
			
			for g in range(0,suc[2]): #chedck to see if successors is valid
				if(p_successors[g] not in frontier):
					if(p_successors[g].depth <= i):
						nex = p_successors[g]
						deck.append(nex)
						frontier.add(nex)
						p_size += 1
						if(goal_test(nex,endpos) == True): #if you find goal
							cost = extract_cost(nex)
							tn += p_size
							c_max = len(deck)
							if(mmax < c_max):
								mmax = c_max
								c_max = c_max - 1
							iters += 1
							return nex, tn, mmax, iters, nex.depth, cost
			tn += p_size
			c_max = len(deck)
			if(len(deck) == 0):
				brk = True
			else:
				current = deck.pop()
			frontier.add(current)
			if(mmax < c_max):
				mmax = c_max
			c_max = c_max - 1
			iters += 1
			


def breadth_first_search(grid, startpos, endpos):
	# Perform breadth-first search
	# Goal test at generation
	current = node( None, startpos, 0, 0)
	tn = 1 #total_nodes_generated
	c_max = 0 #current_nodes_stored
	mmax = 0 #max number of nodes stored
	iters = 0 #num_iterations
	deck = deque() #acts as a stack in this case
	frontier = Set() #Stores Locations added to frontier
	explored = Set() #Stores locations already explored
	sat = Set()
	goal = False

	frontier.add(current)
	while(goal == False):
		frontier.remove(current)
		explored.add(current.position)
		suc = generation(current,grid,endpos,explored,0)
		p_successor = suc[0]
		p_size = 0
		for i in range(0,suc[2]):
			if (p_successor[i] not in frontier):
				nex = p_successor[i]
				deck.append(nex)
				frontier.add(nex)
				p_size += 1
				if(goal_test(nex,endpos) == True):
					cost = extract_cost(nex)
					goal = True
					tn += p_size
					c_max = len(deck)
					if(mmax < c_max):
						mmax = c_max
						c_max = c_max - 1
					iters += 1
					return nex, tn, mmax, iters, nex.depth, cost
		tn += p_size
		c_max = len(deck)
		current = deck.popleft() #pop letf to simulate queue
		frontier.add(current)
		if(mmax < c_max):
			mmax = c_max
		c_max = c_max - 1
		iters += 1

	# Return all of the following
	#return #goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal

def uniform_cost_search(grid, startpos, endpos):
	# Perform uniform cost search
	# Goal test at expansion
	current = node(None,startpos,0,0)
	tn = 1 #total nodes stored
	c_max = 0 #current nodes stored
	mmax = 0
	iters = 0
	deck = MinHeap()
	sat = Set()
	while(goal_test(current,endpos) == False):
		#print current.position
		suc = get_successors(current,grid,endpos,sat,zero_heuristic)
		size = suc[2]
		s = suc[0]
		sat.update(suc[1])
		#print "number of additions",size
		#print suc[1]
		#print sat
		for i in range(0,size):
			deck.push(s[i])
		tn += suc[2]
		c_max = len(deck)
		#print len(deck)
		current = deck.top()
		deck.pop()
		if(mmax < c_max):
			mmax = c_max
		c_max = c_max - 1
		iters += 1
	# Return all of the following
	cost = 0
	cost = extract_cost(current)
	return current, tn, mmax, iters, current.depth, cost
	return #goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal
	
def a_star_search(grid, startpos, endpos, heuristic=manhattan):
	# Perform A* search
	# Goal test at expansion
	her = heuristic(startpos,endpos)
	current = node(None,startpos,0,her)
	tn = 1
	c_max = 0
	mmax = 0
	iters = 0
	deck = MinHeap()
	sat = Set()
	while(goal_test(current,endpos) == False):
		suc = get_successors(current,grid,endpos,sat,heuristic)
		size = suc[2]
		s = suc[0]
		sat.update(suc[1])
		for i in range(0,size):
			deck.push(s[i])
		tn += suc[2]
		c_max = len(deck)
		current = deck.top()
		deck.pop()
		if(mmax < c_max):
			mmax = c_max
		c_max = c_max - 1
		iters += 1
	cost = 0
	cost = extract_cost(current)
	return current, tn, mmax, iters, current.depth, cost
	# Return all of the following
	return #goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal


