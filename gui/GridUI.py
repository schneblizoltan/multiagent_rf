from math import floor
from time import sleep
from tkinter import Tk, Canvas, Frame, BOTH
from gui.Colors import Colors

class GridUI(Frame):

	FRAME_TITLE = "GridWorld"

	def __init__(self, parent, height, width, cellSize, grid, robots, frontier):
		Frame.__init__(self, parent)
		self.parent = parent
		self.initializeFrame(parent, height, width, cellSize)
		self.initializeGrid(height, width, cellSize, grid, robots, frontier)

	def initializeFrame(self, frame, height, width, cellSize):
		frameHeight = str((height + 2) * cellSize)
		frameWidth = str((width + 2) * cellSize)
		xOffset, yOffset = self.getOffsets(height, width)
		geometryParameters = frameWidth + 'x' + frameHeight + '+' + str(xOffset) + '+' + str(yOffset)
		
		frame.geometry(geometryParameters)

	def initializeGrid(self, height, width, cellSize, grid, robots, frontier):
		self.parent.title(GridUI.FRAME_TITLE)
		self.pack(fill = BOTH, expand = 1)

		self.canvas = Canvas(self)

		startX = cellSize
		startY = cellSize
		endX = startX + (cellSize * width)
		endY = startY + (cellSize * height)

		curX = startX
		curY = startY
		xIdx = 0
		yIdx = 0

		while curX != endX and curY != endY:
			self.drawRectangles(grid, curX, curY, xIdx, yIdx, cellSize, robots, frontier)
			
			curX = curX + cellSize
			if curX == endX and curY != endY:
				curX = startX
				xIdx += 1
				curY = curY + cellSize
				yIdx = 0
				continue
			elif curX == endX and curY == endY:
				break
			yIdx += 1

		self.canvas.pack(fill = BOTH, expand = 1)

	def redraw(self, height, width, cellSize, grid, robots, frontier):
		self.parent.title(GridUI.FRAME_TITLE)
		self.pack(fill = BOTH, expand = 1)

		self.canvas.delete('all')

		startX = cellSize
		startY = cellSize
		endX = startX + (cellSize * width)
		endY = startY + (cellSize * height)

		curX = startX
		curY = startY
		xIdx = 0
		yIdx = 0

		while curX != endX and curY != endY:
			self.drawRectangles(grid, curX, curY, xIdx, yIdx, cellSize, robots, frontier)
			
			curX = curX + cellSize
			if curX == endX and curY != endY:
				curX = startX
				xIdx += 1
				curY = curY + cellSize
				yIdx = 0
				continue
			elif curX == endX and curY == endY:
				break
			yIdx += 1

		self.canvas.pack(fill = BOTH, expand = 1)

	def drawRectangles(self, grid, curX, curY, xIdx, yIdx, cellSize, robots, frontier):
		robotFlag = self.drawRobotRectangles(curX, curY, xIdx, yIdx, cellSize, robots)

		if self.isObstacle(grid, xIdx, yIdx):
			self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = Colors.OUTLINE, fill = Colors.OBSTACLE, width = 2)	
		elif robotFlag == False:
			frontierFlag = self.drawFrontierRectangles(curX, curY, xIdx, yIdx, cellSize, frontier, grid)

			if frontierFlag == False:
				if self.isVisited(grid, xIdx, yIdx):
					self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = Colors.OUTLINE, fill = Colors.VISITED, width = 2)
				else:
					self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = Colors.OUTLINE, fill = Colors.UNVISITED, width = 2)

	def drawRobotRectangles(self, curX, curY, xIdx, yIdx, cellSize, robots):
		robotFlag = False
		for robot in robots:
			if robot.curX == xIdx and robot.curY == yIdx:
				robotFlag = True
				self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = Colors.OUTLINE, fill = Colors.AGENT, width = 2)

		return robotFlag

	def drawFrontierRectangles(self, curX, curY, xIdx, yIdx, cellSize, frontier, grid):
		frontierFlag = False
		for pt in frontier:
			if pt[0] == xIdx and pt[1] == yIdx:
				self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = Colors.OUTLINE, fill = Colors.FRONTIER, width = 2)
				frontierFlag = True

		return frontierFlag

	def isObstacle(self, grid, xIdx, yIdx):
		return grid.cells[xIdx][yIdx].obstacle

	def isVisited(self, grid, xIdx, yIdx):
		return grid.cells[xIdx][yIdx].visited

	def getOffsets(self, height, width):
		xOffset = 100
		yOffset = 100
		if height <= 10:
			xOffset = 300
		if width <= 10:
			yOffset = 300

		return (xOffset, yOffset)