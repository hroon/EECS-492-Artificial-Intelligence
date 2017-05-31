#Haroon Syed
#haroons
from numpy.random import randint
from numpy.random import shuffle
from copy import copy,deepcopy

# Manhattan distance between curpos and endpos (tuples)
def manhattan(curpos, endpos):
	return abs(endpos[0]-curpos[0])+abs(endpos[1]-curpos[1])

#prints the grid
def printmat(mat):
	for i in range(0,3):
		print mat[i][0],mat[i][1],mat[i][2]
	print '\n'
def findpos(curvalue, goal):
	for i in range(0,3):
		for d in range(0,3):
			if (curvalue == goal[i][d]):
				return (i,d)

#makes sure the position is on the grid
def check(position):
	x = position[0]
	y = position[1]
	a = True 
	if(x < 0 or y < 0):
		return False
	if(x <= 2 and y <=2):
		return True
	return False

#compares two grids and 
#finds the heuristic using the manhattan distance
def cost(init,goal):
	cost = 0
	total = 0
	for j in range(0,3):
		for k in range(0,3):
			#print (j,k)
			val = init[j][k]
			gp = findpos(val,goal)
			cur = (j,k)
			cost = manhattan(cur,gp)
			if (val == 0):
				cost = 0
			#print cost
			total += cost
	return total

#gets the successors and returns the best one
def move(starting,heuristic,goal):
	initial = findpos(0,starting)
	other = None
	x = initial[0] #row
	y = initial[1] #column
	new1 = None
	north = (x-1, y)
	east = (x, y+1)
	south = (x+1, y)
	west = (x, y-1)
	cur_min = copy(heuristic)
	pathcost = 0
	plateau = False
	if(check(north)):
		#print 'north'
		other = deepcopy(starting)
		val1 = other[x-1][y]
		other[x-1][y] = 0
		other[x][y] = val1
		#printmat(other)
		pathcost = cost(other,goal)
		#print pathcost
		if(pathcost < cur_min):
			cur_min = pathcost
			new1 = deepcopy(other)
	if(check(east)):
		#print 'east'
		other = deepcopy(starting)
		val1 = other[x][y+1]
		other[x][y+1] = 0
		other[x][y] = val1
		#printmat(other)
		pathcost = cost(other,goal)
		#print pathcost
		if(pathcost < cur_min):
			cur_min = pathcost
			new1 = copy(other)
	if(check(south)):
		other = deepcopy(starting)
		val1 = other[x+1][y]
		other[x+1][y] = 0
		other[x][y] = val1
		pathcost = cost(other,goal)
		#print pathcost
		if(pathcost < cur_min):
			cur_min = pathcost
			new1 = copy(other)
	if(check(west)):
	#	print 'west'
		other = deepcopy(starting)
		val1 = other[x][y-1]
		other[x][y-1] = 0
		other[x][y] = val1
		pathcost = cost(other,goal)
		#print pathcost
		#printmat(other)
		if(pathcost < cur_min):
			cur_min = pathcost
			new1 = copy(other)
	if(cur_min == heuristic):
		plateau = True
	#plateau = True
	return new1, cur_min, plateau

	
grid = [[0 for x in range(3)] for y in range(3)]
goal = deepcopy(grid)
goal[0][0] = 0
goal[0][1] = 1
goal[0][2] = 2
goal[1][0] = 3
goal[1][1] = 4
goal[1][2] = 5
goal[2][0] = 6
goal[2][1] = 7
goal[2][2] = 8
printmat(goal)
inital = None
line = [0,1,2,3,4,5,6,7,8]
mats = []
size = 0
plateau = False
for i in range(0,25000):
	shuffle(line)
	#line = [4,5,7,1,2,8,3,0,6]
	grid[0][0] = line[0]
	grid[0][1] = line[1]
	grid[0][2] = line[2]
	grid[1][0] = line[3]
	grid[1][1] = line[4]
	grid[1][2] = line[5]
	grid[2][0] = line[6]
	grid[2][1] = line[7]
	grid[2][2] = line[8]
	orig = deepcopy(grid)
	initial = deepcopy(grid)
	#printmat(initial)
	minimum = cost(initial,goal)
	#print minimum
	#second = 1000;
	new_pos = None
	plateau = False
	while(plateau == False):
		#print minimum
		suc = move(initial,minimum,goal)
		minimum = suc[1]
		plateau = suc[2]
		initial = deepcopy(suc[0])
		if(minimum == 0):
			mats.append(orig)
			size += 1
			plateau = True
		
		#print plateau

print 'goals found:', size
for i in range(0,size):
	printmat(mats[i])
