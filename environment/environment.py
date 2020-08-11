import math
import random
import sys
import numpy as np

from gui.Grid import Grid
from agents.Agent import Agent


class Environment:

	ACTION_NR = 4					# Number of action wich the agent knows about: N, E, S, W
	STATE_NR = 5					# Number of states defined

	def __init__(self, height, width, gridworld, agents = []):
		self.gridworld = gridworld
		self.action_n = Environment.ACTION_NR
		self.state_n = Environment.STATE_NR
		self.height = height
		self.width = width
		self.reward_matrix = np.zeros((self.state_n, self.action_n)).astype("float32")
		self.reward_matrix = self.getRewardMatrix()
		self.completedFlag = False
		self.frontier = []

	def updateFrontiers(self):
		self.frontier = self.computeFrontier()

	def getState(self, id):
		cell = self.getValidCell(self.agents[id], -1, 0)
		if cell != None and (cell.occupied == True or cell.obstacle == True):
			return 1
		cell = self.getValidCell(self.agents[id], 1, 0)
		if cell != None and (cell.occupied == True or cell.obstacle == True):
			return 2
		cell = self.getValidCell(self.agents[id], 0, -1)
		if cell != None and (cell.occupied == True or cell.obstacle == True):
			return 3
		cell = self.getValidCell(self.agents[id], 0, 1)
		if cell != None and (cell.occupied == True or cell.obstacle == True):
			return 4
		return 0

	def getRewardMatrix(self):
		# Action order: W, E, N, S

		# State 0 - No agent and wall above, left, right, down and nothing discovered around
		self.reward_matrix[0,:] = [1, 1, 1, 1]

		# State 1 - Agent/wall above, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[1,:] = [1, 1, -1, 1]
		
		# State 2 - Agent/wall below, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[2,:] = [1, 1, 1, -1]

		# State 3 - Agent/wall left, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[3,:] = [-1, 1, 1, 1]
		
		# State 4 - Agent/wall right, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[4,:] = [1, -1, 1, 1]

		return self.reward_matrix

	# Method to print(the current grid to the output descriptor)
	def printGrid(self):

		for i in range(self.height):
			for j in range(self.width):
				# If the current cell is an obstacle, print(#)
				if self.gridworld.cells[i][j].obstacle == True:
					sys.stdout.write(' # ')
				# If the current cell is occupied by an agent, print(its id)
				elif self.gridworld.cells[i][j].occupied == True:
					agentId = 0
					for agent in self.agents:
						if agent.curX == i and agent.curY == j:
							agentId = agent.id
					temp = ' ' + str(agentId) + ' '
					sys.stdout.write(temp)
				# If the current cell is a frontier, print(a |)
				elif (i, j) in self.frontier:
					sys.stdout.write(' | ')
				# Otherwise, print(-)
				else:
					if self.gridworld.cells[i][j].visited == True:
						sys.stdout.write(' . ')
					else:
						sys.stdout.write(' - ')
			sys.stdout.write('\n')

	# Method to compute the frontiers
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

	def getMovesFromAction(self, action):
		if action == 0:		# Left
			return (0, -1)
		if action == 1:		# Right
			return (0, 1)
		if action == 2:		# Up
			return (-1, 0)
		if action == 3:		# Down
			return (1, 0)

	def getValidCell(self, agent, moveX, moveY):
		if agent.curX + moveX > 0 and agent.curX + moveX < self.width and agent.curY + moveY > 0 and agent.curY + moveY < self.height:
			return self.gridworld.cells[agent.curX + moveX][agent.curY + moveY]
		return None

	def step(self, id, action):
		(moveX, moveY) = self.getMovesFromAction(action)
		cell = self.getValidCell(self.agents[id], moveX, moveY)
		if cell != None and cell.occupied == False and cell.obstacle == False:
			self.gridworld.cells[self.agents[id].curX][self.agents[id].curY].occupied = False
			self.agents[id].setLocation(self.agents[id].curX + moveX, self.agents[id].curY + moveY)
			self.gridworld.cells[self.agents[id].curX][self.agents[id].curY].visited = True
			self.gridworld.cells[self.agents[id].curX][self.agents[id].curY].occupied = True
			
		return 1, False

	def runOneIter(self):
		for i in range(len(self.agents)):
			self.agents[i].step(self)
		self.updateFrontiers()

	def isExplored(self):
		if self.frontier:
			return False
		return True