import math
import random
import sys
import numpy as np

from gui.Grid import Grid
from agents.Agent import Agent


class Environment:

	ACTION_NR = 4					# Number of action wich the agent knows about: N, E, S, W
	STATE_NR = 25					# Number of states defined

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
		frontierCells = self.computeFrontier()
		cellUp = self.getValidCell(self.agents[id], -1, 0)
		cellDown = self.getValidCell(self.agents[id], 1, 0)
		cellRight = self.getValidCell(self.agents[id], 0, -1)
		cellLeft = self.getValidCell(self.agents[id], 0, 1)

		if (((self.agents[id].curX, self.agents[id].curY + 1) in frontierCells) and ((self.agents[id].curX, self.agents[id].curY - 1) in frontierCells)) is True:
			return 9
		if (((self.agents[id].curX, self.agents[id].curY + 1) in frontierCells) and ((self.agents[id].curX - 1, self.agents[id].curY) in frontierCells)) is True:
			return 10
		if (((self.agents[id].curX, self.agents[id].curY + 1) in frontierCells) and ((self.agents[id].curX + 1, self.agents[id].curY) in frontierCells)) is True:
			return 11

		if (((self.agents[id].curX, self.agents[id].curY - 1) in frontierCells) and ((self.agents[id].curX - 1, self.agents[id].curY) in frontierCells)) is True:
			return 12
		if (((self.agents[id].curX, self.agents[id].curY - 1) in frontierCells) and ((self.agents[id].curX + 1, self.agents[id].curY) in frontierCells)) is True:
			return 13

		if (((self.agents[id].curX - 1, self.agents[id].curY) in frontierCells) and ((self.agents[id].curX + 1, self.agents[id].curY) in frontierCells)) is True:
			return 14

		if (self.agents[id].curX, self.agents[id].curY + 1) in frontierCells:
			return 5
		if (self.agents[id].curX, self.agents[id].curY - 1) in frontierCells:
			return 6
		if (self.agents[id].curX - 1, self.agents[id].curY) in frontierCells:
			return 7
		if (self.agents[id].curX + 1, self.agents[id].curY) in frontierCells:
			return 8

		if cellRight != None and (cellRight.occupied == True or cellRight.obstacle == True) and cellLeft != None and (cellLeft.occupied == True or cellLeft.obstacle == True):
			return 20

		if (cellLeft == None or (cellLeft.occupied == True or cellLeft.obstacle == True)) and (cellUp == None or (cellUp.occupied == True or cellUp.obstacle == True)):
			return 21

		if (cellLeft == None or (cellLeft.occupied == True or cellLeft.obstacle == True)) and (cellDown == None or (cellDown.occupied == True or cellDown.obstacle == True)):
			return 22

		if (cellRight == None or (cellRight.occupied == True or cellRight.obstacle == True)) and (cellUp == None or (cellUp.occupied == True or cellUp.obstacle == True)):
			return 23

		if (cellRight == None or (cellRight.occupied == True or cellRight.obstacle == True)) and (cellDown == None or (cellDown.occupied == True or cellDown.obstacle == True)):
			return 24

		if cellUp != None and cellDown != None and cellLeft != None and cellRight != None and (cellUp.occupied == True or cellUp.obstacle == True) and cellDown.visited == True and cellLeft.visited == True and cellRight.visited == True:
			return 16
		if cellUp != None and cellDown != None and cellLeft != None and cellRight != None and (cellDown.occupied == True or cellDown.obstacle == True) and cellUp.visited == True and cellLeft.visited == True and cellRight.visited == True:
			return 17
		if cellUp != None and cellDown != None and cellLeft != None and cellRight != None and (cellRight.occupied == True or cellRight.obstacle == True) and cellDown.visited == True and cellLeft.visited == True and cellUp.visited == True:
			return 18
		if cellUp != None and cellDown != None and cellLeft != None and cellRight != None and (cellLeft.occupied == True or cellLeft.obstacle == True) and cellDown.visited == True and cellUp.visited == True and cellRight.visited == True:
			return 19
			
		if (cellUp == None or (cellUp.occupied == True or cellUp.obstacle == True)):
			return 1
		if (cellDown == None or (cellDown.occupied == True or cellDown.obstacle == True)):
			return 2
		if (cellRight == None or (cellRight.occupied == True or cellRight.obstacle == True)):
			return 3
		if (cellLeft == None or (cellLeft.occupied == True or cellLeft.obstacle == True)):
			return 4

		if cellUp != None and cellDown != None and cellLeft != None and cellRight != None and cellUp.visited == True and cellDown.visited == True and cellLeft.visited == True and cellRight.visited == True:
			return 15

		return 0

	def getRewardMatrix(self):
		# Action order: Left, Right, Up, Down

		# State 0 - No agent and wall above, left, right, down and nothing discovered around
		self.reward_matrix[0,:] = [1, 1, 1, 1]

		# State 1 - Agent/wall above, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[1,:] = [1, 1, -10, 1]
		
		# State 2 - Agent/wall below, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[2,:] = [1, 1, 1, -10]

		# State 3 - Agent/wall left, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[3,:] = [-10, 1, 1, 1]
		
		# State 4 - Agent/wall right, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[4,:] = [1, -10, 1, 1]

		# State 5 - Frontier right, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[5,:] = [0, 2, 0, 0]

		# State 6 - Frontier left, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[6,:] = [2, 0, 0, 0]

		# State 7 - Frontier up, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[7,:] = [0, 0, 2, 0]

		# State 8 - Frontier down, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[8,:] = [0, 0, 0, 2]

		# State 9 - Frontier left-right, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[9,:] = [2, 2, 0, 0]

		# State 10 - Frontier up-right, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[10,:] = [0, 2, 2, 0]

		# State 11 - Frontier down-right, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[11,:] = [0, 2, 0, 2]

		# State 12 - Frontier left-up, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[12,:] = [2, 0, 2, 0]

		# State 13 - Frontier left-down, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[13,:] = [2, 0, 0, 2]
		
		# State 14 - Frontier up-down, no agent and wall left, right, down and nothing discovered around
		self.reward_matrix[14,:] = [0, 0, 2, 2]

		# State 15 - No agent and wall above, left, right, down and everything discovered around
		self.reward_matrix[15,:] = [-0.5, -0.5, -0.5, -0.5]

		# State 16 - Agent/wall above, no agent and wall left, right, down and everything discovered around
		self.reward_matrix[16,:] = [-0.5, -0.5, -10, -0.5]
		
		# State 17 - Agent/wall below, no agent and wall left, right, down and everything discovered around
		self.reward_matrix[17,:] = [-0.5, -0.5, -0.5, -10]

		# State 18 - Agent/wall left, no agent and wall left, right, down and everything discovered around
		self.reward_matrix[18,:] = [-10, -0.5, -0.5, -0.5]
		
		# State 19 - Agent/wall right, no agent and wall left, right, down and everything discovered around
		self.reward_matrix[19,:] = [-0.5, -10, -0.5, -0.5]

		# State 20 - Wall right and left
		self.reward_matrix[20,:] = [-10, -10, -0.5, -0.5]
		
		# State 21 - Left upper corner
		self.reward_matrix[21,:] = [-10, -0.5, -10, -0.5]
		
		# State 22 - Left down corner
		self.reward_matrix[22,:] = [-10, -0.5, -0.5, -10]
		
		# State 23 - Right upper corner
		self.reward_matrix[23,:] = [-0.5, -10, -10, -0.5]
		
		# State 24 - Right down corner
		self.reward_matrix[24,:] = [-0.5, -10, -0.5, -10]
		
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
		if self.gridworld.inGrid((agent.curX + moveX, agent.curY + moveY)):
		# if agent.curX + moveX > 0 and agent.curX + moveX < self.width and agent.curY + moveY > 0 and agent.curY + moveY < self.height:
			return self.gridworld.cells[agent.curX + moveX][agent.curY + moveY]
		return None

	def step(self, id, state, action):
		frontierCells = self.computeFrontier()
		(moveX, moveY) = self.getMovesFromAction(action)
		cell = self.getValidCell(self.agents[id], moveX, moveY)
		if cell != None and cell.occupied == False and cell.obstacle == False:
			self.gridworld.cells[self.agents[id].curX][self.agents[id].curY].occupied = False
			self.agents[id].setLocation(self.agents[id].curX + moveX, self.agents[id].curY + moveY)
			self.gridworld.cells[self.agents[id].curX][self.agents[id].curY].visited = True
			self.gridworld.cells[self.agents[id].curX][self.agents[id].curY].occupied = True
			
		reward = self.getRewardMatrix()[state, action] 
		if cell != None and (cell.x, cell.y) in frontierCells:
			reward += 10
		
		return reward, self.isExplored()

	def runOneIter(self):
		for i in range(len(self.agents)):
			self.agents[i].step(self)
		self.updateFrontiers()

	def isExplored(self):
		if self.frontier:
			return False
		return True