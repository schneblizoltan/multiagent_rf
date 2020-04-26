import math
import random
import sys
import numpy as np

from gui.Grid import Grid
from agents.Agent import Agent


class Environment:

	# Number of action wich the agent knows about: N, NW, NE, SW, E, SE, S, W
	ACTION_NR = 8
	# Number of states defined
	STATE_NR = 13										   


	def __init__(self, height, width, gridworld, agents = []):
		self.gridworld = gridworld
		self.action_n = Environment.ACTION_NR
		self.state_n = Environment.STATE_NR
		self.height = height
		self.width = width
		self.reward_matrix = np.zeros((self.state_n, self.action_n)).astype("float32")
		self.reward_matrix = self.get_reward_matrix()
		self.completedFlag = False
		self.frontier = []

	def get_reward_matrix(self):
		# Action order: N, NW, NE, SW, E, SE, S, W

		# State 0 - No enemy in front, no block above, no block in front
		self.reward_matrix[0,:] = [-1, 1, 0, -1, 0, 1, 1, 1]

		# State 1 - Block above, no enemy in front, no enemy in back
		self.reward_matrix[1,:] = [-1, 0.9, 1, -1, 1, 1, 1, 1]

		# State 2 - Enemy in front in 1? tile range, no tiles above / tiles above
		self.reward_matrix[2,:] = [-1, -1, +1, -1, 0.9, 1, 1, 1]

		# State 3 - Small obstacle
		self.reward_matrix[3,:] = [-1, -1, -1, -1, 1, 1, 1, 1]

		# State 4 - Large obstacle in front
		self.reward_matrix[4,:] = [0.9, -1, 0, -0.5, 1, 1, 1, 1]

		# State 5 - Block above, enemy in front: range >= 2 tiles
		self.reward_matrix[5,:] = [-1, 0.9, 1, -1, 0.9, 1, 1, 1]

		# State 6 - In air
		self.reward_matrix[6,:] = [0.1, 1, 0, -1, 0, 1, 1, 1]

		# State 7 - No floor in front
		self.reward_matrix[7,:] = [-1, -1, -1, -1, 1, 1, 1, 1]

		# State 8 - Stuck in front of pipe
		self.reward_matrix[8,:] = [1, -1, -1, -0.5, 1, 1, 1, 1]

		# State 9 - Enemy behind 1 tile
		self.reward_matrix[9,:] = [-1, -1, 1, -1, -1, 1, 1, 1]

		# State 10 - Stuck in front of pipe while in air
		self.reward_matrix[10,:] = [1, -1, -1, -0.8, -1, 1, 1, 1]

		# State 11 - Stuck in front of mini pipe
		self.reward_matrix[11,:] = [-1, -1, -1, -1, 1, 1, 1, 1]

		# State 12 - Enemy in front while in air
		self.reward_matrix[12,:] = [1, -1, -1, -1, -1, 1, 1, 1]

		return self.reward_matrix

	# Method to print(the current grid to the output descriptor)
	def printGrid(self):

		## Comment this later
		frontier = self.computeFrontier()

		for i in range(self.height):
			for j in range(self.width):
				# If the current cell is an obstacle, print(#)
				if self.gridworld.cells[i][j].obstacle == True:
					sys.stdout.write(' # ')
				# If the current cell is occupied by an agent, print(its id)
				elif self.gridworld.cells[i][j].occupied == True:
					robotId = 0
					for robot in self.agents:
						if robot.curX == i and robot.curY == j:
							robotId = robot.id
					temp = ' ' + str(robotId) + ' '
					sys.stdout.write(temp)
				# If the current cell is a frontier, print(a |)
				elif (i, j) in frontier:
					sys.stdout.write(' | ')
				# Otherwise, print(-)
				else:
					if self.gridworld.cells[i][j].visited == True:
						sys.stdout.write(' . ')
					else:
						sys.stdout.write(' - ')
			sys.stdout.write('\n')

	# Method to compute the frontier
	def computeFrontier(self):

		frontier = []

		# Iterate over all cells in the grid
		for i in range(self.height):
			for j in range(self.width):
				# We compute 8-neighbors for only those cells that haven't been visited or are obstacles
				# Only such cells are possible candidates for the frontier
				if self.gridworld.cells[i][j].visited == False and self.gridworld.cells[i][j].obstacle == False:
					point = (i, j)
					neighbors = self.gridworld.get8Neighbors(point)
					# Now we see if there is at least one neighbor of the current cell which has been visited
					# In such a case, the current cell would become a frontier cell
					frontierFlag = False
					for nbhr in neighbors:
						if self.gridworld.cells[nbhr[0]][nbhr[1]].visited == True:
							frontierFlag = True

					if frontierFlag == True:
						frontier.append((i, j))

		return frontier
