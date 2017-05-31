#Haroon Syed

import numpy as np 
import sys
import copy

def printmatrix(state,nrows,ncols,hazards,initial):
	for i in range(nrows):
		sys.stdout.write('\n')
		for j in range(0,ncols):
			if(hazards[i][j] == 1):
				sys.stdout.write('x ')
			elif(hazards[i][j] == 2):
				sys.stdout.write(initial[i][j])
			else:
				temp = format(state[i][j], '.3f')
				sys.stdout.write(str(temp))
				sys.stdout.write(' ')
	print '\n'
	sys.stdout.flush()


def check(position, nrows,ncols, hazards):
	x = position[0]
	y = position[1]

	if(x < 0 or y < 0):
		return False
	if(x < nrows and y < ncols):
		if(hazards[x][y] == 1): #if there is a wall
			return False
		else:
			return True

	return False



#returns max sum 
def action(current,trans,nrows,ncols,U,hazards):
	x = current[0]
	y = current[1]

	p1 = trans[0]
	p2 = trans[1]
	p3 = trans[2]
	p4 = trans[3]

	north = (x-1,y)
	east = (x,y+1)
	south = (x+1,y)
	west = (x,y-1)

	if (check(north,nrows,ncols,hazards) == False):	#stay at same location if hit a wall
		north = current
	if (check(east,nrows,ncols,hazards) == False):
		east = current
	if (check(south,nrows,ncols,hazards) == False):
		south = current
	if (check(west,nrows,ncols,hazards) == False):
		west = current


	n1 = north[0]
	n2 = north[1]
	e1 = east[0]
	e2 = east[1]
	s1 = south[0]
	s2 = south[1]
	w1 = west[0]
	w2 = west[1]

	up = p1*U[n1][n2] + p2*U[e1][e2] + p3*U[s1][s2] + p4*U[w1][w2]
	right = p1*U[e1][e2] + p2*U[s1][s2] + p3*U[w1][w2] + p4*U[n1][n2]
	down = p1*U[s1][s2] + p2*U[w1][w2] + p3*U[n1][n2] + p4*U[e1][e2]
	left = p1*U[w1][w2] + p2*U[n1][n2] + p3*U[e1][e2] + p4*U[s1][s2]


	maximum = max(up,right,down,left)
	return maximum
	


#returns a utlity function
def value_iteration(states,trans, e, R, gam,nrows,ncols,hazards):
	#local variables, 
	U = [[0 for x in range(ncols)] for y in range(nrows)] #vector
	for q in range(nrows):
		for y in range(ncols):
			if(states[q][y] != 'x' and states[q][y] != '*'):
				U[q][y] = float(states[q][y])
	Up = copy.deepcopy(U) #vectors of utilities for states initially 0
	#d = float(e)*(1-float(gam))/float(gam) #max change of utility of any state
	d = 0.0001
	it = 0
	done = False
	#while(d >= float(e)*(1-gam)/gam): #should probably change soon
	while(done == False):
		it += 1
		U = copy.deepcopy(Up)
		done = True
		#printmatrix(U,nrows,ncols)
		for i in range(0,nrows):
			for j in range(0,ncols):
				if(hazards[i][j] == 0): #if not a wall or a reward state
					cur = (i,j)
					Up[i][j] = R + gam*action(cur,trans,nrows,ncols,U,hazards)
					if(abs(Up[i][j] - U[i][j]) >= d):
						done = False
						#d = Up[i][j] - U[i][j]
		##print it

	return U




if __name__ == '__main__':
	assert(len(sys.argv) == 2)
	file = sys.argv[1]
	f = open(file, 'r')
	gamma = float(f.readline()) #discount factor gamma
	col = float(f.readline()) #cost of living
	trans = f.readline() #transition probabilities in order, n, e, s, w
	trans = [float(x) for x in trans.split()]
	nrows = 0
	ncols = 0
	e = 0.01
	#if (gamma == 1):
	#	gamma = 0.999999
	space = list() #state space
	for line in f:
		ncols = 0
		nrows += 1
		space.append([x for x in line.split()])
		for a in line.split():
			ncols += 1

	hazards = copy.deepcopy(space) #keeps track of walls and big rewards
	for i in range(0,nrows):
		for j in range(0,ncols):
			if (space[i][j] == '*'):
				hazards[i][j] = 0
			else:
				hazards[i][j] = 2

			if(space[i][j] == 'x'):
				hazards[i][j] = 1

	
	
	U = value_iteration(space, trans, e, col,gamma,nrows,ncols,hazards)
	printmatrix(U,nrows,ncols,hazards,space)