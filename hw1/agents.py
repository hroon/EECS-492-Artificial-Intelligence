# Haroon Syed
# EECS 492 Homework 1

import world
from numpy.random import randint

class simple_reflex_agent:
	def __init__(self):
		# Agent has no state, so nothing to do here
		return

	# Given a valid percept (a string), return a valid action (also as a string)
	def choose_action(self, percept):
		##### Implement this function #####
		word = percept
		if word == 'hit_barrier':
			return 'move'
		else:
			if (word == 'start' or word == 'move_succeeded'):
				return 'sense_water'
			if word == 'does_not_need_watering':
				return 'sense_weed'
			if word == 'needs_watering':
				return 'water'
			if word == 'watering_succeeded':
				return 'sense_weed'
			if word == 'does_not_need_weeding':
				return 'move'
			if word == 'needs_weeding':
				return 'weed'
			if word == 'weeding_succeeded':
				return 'move'
			

		# Returning an arbitrary action so don't get import errors if function not written
		# You may remove this when you've finished implementing
		#################################


class state_reflex_agent:
	def __init__(self, worldstate):
		# This agent has a state, so wants to do BFS on the world
		# self.plan is a list of moves for the agent to take through the world
		# self.position is the position in the list
		self.plan, plan_exists = world.BFS(worldstate)
		if not plan_exists:
			raise RuntimeError('Plan does not exist or BFS iteration limit exceeded')
		self.position = 0

	# Given a valid percept (a string), return a valid action (also as a string)
	def choose_action(self, percept):
		#### Implement this function ####
		word = percept
		if word == 'move_succeeded':
			return 'sense_water'
		if (word == 'does_not_need_weeding' or word == 'weeding_succeeded'):
			old = self.position #iterating through positions
			self.position = (self.position + 1)
			return self.plan[old]
		if (word == 'start' or word == 'move succeeded'):
			return 'sense_water'
		if word == 'does_not_need_watering':
			return 'sense_weed'
		if word == 'needs_watering':
			return 'water'
		if word == 'watering_succeeded':
			return 'sense_weed'
		if word == 'needs_weeding':
			return 'weed'



		# Returning an arbitrary action so don't get import errors if function not written
		# You may remove this when you've finished implementing
		#################################

class random_reflex_agent:
	def __init__(self):
		# Agent has no state, so nothing to do here
		return

	# Given a valid percept (a string), return a valid action (also as a string)
	def choose_action(self, percept):
		#### Implement this function ####
		mat = ['move_east', 'move_west', 'move_north', 'move_south']
		word = percept
		if word == 'move_succeeded':
			return 'sense_water'
		if (word == 'does_not_need_weeding' or word == 'weeding_succeeded'):
			num = randint(0,4)
			return mat[num]
		if (word == 'start' or word == 'move succeeded'):
			return 'sense_water'
		if word == 'does_not_need_watering':
			return 'sense_weed'
		if word == 'needs_watering':
			return 'water'
		if word == 'watering_succeeded':
			return 'sense_weed'
		if word == 'needs_weeding':
			return 'weed'











		# Returning an arbitrary action so don't get import errors if function not written
		# You may remove this when you've finished implementing
		return 'water'
		#################################
def isBarrier(x,y,move,barrier,size): #checks if it will hit a past barrier
	a = x
	b = y
	if move == 0: #north
		y += 1
	if move == 1: #east
		x += 1
	if move == 2: #south
		y -= 1
	if move == 3: #west
		x -= 1
	for i in range(0,size):
		if [x,y] == barrier[i]:
			x = a
			y = b
			return True #there is a barrier
	return False
class better_reflex_agent:
	def __init__(self):
		# Agent cannot see the world in advance
		# However, you may initialize any number of your own state variables here
		self.past_locations = [] #remembering where its already been
		self.barriers = [] #remembering barriers
		self.current = [0,0] #current agent location
		self.repeat = 0 #if it keeps moving back and forth
		self.size = 0 #size of past locations list
		self.bsize = 0 #size of barriers list
		self.move = 0 #north/east/south/west
		self.last = [0,0] #previous location

		return

	# Given a valid percept (a string), return a valid action (also as a string)
	def choose_action(self, percept):
		##### Implement this function #####
		# You may store any amount of information about past percepts and actions,
		# use additional state variables, and perform any additional computation 
		# that you see fit, in order to outperform simple_reflex_agent.
		# Do not use randomness, or data structures not built into Python
		# You may only use sense_water, sense_weed, water, weed, and move as actions
		mat = ['move_north', 'move_east', 'move_south', 'move_west']
		word = percept
		if word == 'start':
			return 'sense_water'
		else:
			if word == 'hit_barrier':
				self.repeat += 1;  #make sure it doesnt keep hitting same 
				a = self.current[0]
				b = self.current[1]
				self.barriers.append([a,b]) #adding to barrier list
				self.bsize += 1
				x = self.past[0]
				y = self.past[1]
				self.current = [x,y]
				x = self.current[0]
				y = self.current[1]

				move = self.move
				
				count = 0
				while(isBarrier(x,y,move,self.barriers,self.bsize) == True):
					count += 1
					if move == 3:
						move = 0
					else:
						move += 1
				#move should now be good
				if move == 0:
					y += 1
				if move == 1:
					x += 1
				if move == 2:
					y -= 1
				if move == 3:
					x -= 1

				self.current[0] = x
				self.current[1] = y
				self.move = move
				return mat[move]
			for i in range(0,self.size):
				if (self.current == self.past_locations[i]):
					move = self.move
					x = self.current[0]
					y = self.current[1]
					self.past = [x,y]
					if self.repeat > 6:
						move += 1
					if move > 3:
						move = 0
					count = 0
					while(isBarrier(x,y,move,self.barriers,self.bsize) == True):
						count += 1
						if move == 3:
							move = 0
						else:
							move += 1
					#move should now be good
					if move == 0:
						y += 1
					if move == 1:
						x += 1
					if move == 2:
						y -= 1
					if move == 3:
						x -= 1
					self.current[0] = x
					self.current[1] = y
					return mat[move]
			if (word == 'start' or word == 'move_succeeded'):
				return 'sense_water'
			if (word == 'does_not_need_weeding' or word == 'weeding_succeeded'):
				x = self.current[0]
				y = self.current[1]
				self.past = [x,y]
				self.past_locations.append([x,y])
				self.size += 1
				move = self.move
				x = self.current[0]
				y = self.current[1]
				count = 0
				while(isBarrier(x,y,move,self.barriers,self.bsize) == True):
					count += 1
					if move == 3:
						move = 0
					else:
						move += 1
				#move should now be good
				if move == 0:
					y += 1
				if move == 1:
					x += 1
				if move == 2:
					y -= 1
				if move == 3:
					x -= 1
				self.current[0] = x
				self.current[1] = y
				self.move = move
				return mat[move]
			if word == 'does_not_need_watering':
				self.repeat = 0;
				return 'weed'
			if word == 'needs_watering':
				return 'water'
			if word == 'watering_succeeded':
				return 'sense_weed'
			if word == 'needs_weeding':
				return 'weed'


		# Returning an arbitrary action so don't get import errors if function not written
		# You may remove this when you've finished implementing
		#################################

