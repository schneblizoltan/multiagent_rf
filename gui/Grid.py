from itertools import filterfalse
from gui import Cell

class Grid:

	def __init__(self, width, height, obstacles):
		self.width = width
		self.height = height
		self.cells = [[Cell.Cell(i, j) for j in range(width)] for i in range(height)]
		self.obstacles = obstacles
		for obstacle in self.obstacles:
			self.cells[obstacle[0]][obstacle[1]].obstacle = True

	def inGrid(self, position):
		"""Check if the current (x, y) cell is in the grid or not"""
		(x, y) = position
		return x in range(0, self.height) and y in range(0, self.width)

	def isObstacle(self, id):
		"""Check if the current (x, y) cell is an obstacle or not"""
		(x, y) = id
		return self.cells[x][y].obstacle

	def isDiscovered(self, id):
		"""Check if the current (x, y) cell is discovered or not"""
		(x, y) = id
		return self.cells[x][y].visited

	def getCorrectNeighbours(self, neighbors):
		"""Filters out all neighbouring cells which are not in the grid or are obstacles"""
		neighbors = filter(self.inGrid, neighbors)
		return filterfalse(self.isObstacle, neighbors)

	def get4Neighbors(self, id):
		"""If the current cell is not an obstacle, return a list of all valid neighbours (from the directions N, S, W, E)"""
		(x, y) = id

		if self.cells[x][y].obstacle == True:
			return []

		return self.getCorrectNeighbours([(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)])

	def get8Neighbors(self, id):
		"""If the current cell is not an obstacle, return a list of all valid neighbours (from the directions N, S, W, E, NE, NW, SE, SW)"""
		(x, y) = id

		if self.cells[x][y].obstacle == True:
			return []
		
		return self.getCorrectNeighbours([(x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1)])

	def getDiscoveredPercentage(self):
		allTiles = self.width * self.height - len(self.obstacles)
		discoveredTiles = [(i, j) for j in range(self.width) for i in range(self.height)]
		discoveredTiles = filterfalse(self.isObstacle, discoveredTiles)
		discoveredTiles = [tile for tile in discoveredTiles if self.isDiscovered(tile)]
		return len(discoveredTiles) / allTiles * 100
