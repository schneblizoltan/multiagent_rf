from math import floor
from time import sleep
from tkinter import Tk, Canvas, Frame, BOTH

class GridUI(Frame):

	def __init__(self, parent, height, width, cellSize, grid, robots, frontier):
		Frame.__init__(self, parent)
		self.parent = parent
		self.initialize(height, width, cellSize, grid, robots, frontier)

	def initialize(self, height, width, cellSize, grid, robots, frontier):
		self.parent.title('Grid')
		self.pack(fill = BOTH, expand = 1)

		self.canvas = Canvas(self)

		startX = cellSize
		startY = cellSize
		endX = startX + (cellSize * width)
		endY = startY + (cellSize * height)

		curX = startX
		curY = startY
		rectIdx = 0
		xIdx = 0
		yIdx = 0

		while curX != endX and curY != endY:
			
			# print 'x, y:', xIdx, yIdx
			# First, check if the current location corresponds to that of any robot
			robotFlag = False
			for robot in robots:
				if robot.curX == xIdx and robot.curY == yIdx:
					robotFlag = True
					self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = '#0000FF', fill = '#00FF00', width = 2)
			# Then check if it corresponds to an obstacle
			if grid.cells[xIdx][yIdx].obstacle == True:
				self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = '#0000FF', fill = '#000000', width = 2)	
			elif robotFlag == False:
				# Then check if it corresponds to a frontier cell
				frontierFlag = False
				for pt in frontier:
					if pt[0] == xIdx and pt[1] == yIdx:
						self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = '#0000FF', fill = '#00FFFF', width = 2)
						frontierFlag = True

				if frontierFlag == False:
					if grid.cells[xIdx][yIdx].visited == True:
						self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = '#0000FF', fill = '#FFFFFF', width = 2)
					else:
						self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = '#0000FF', fill = '#777777', width = 2)
			
			curX = curX + cellSize
			if curX == endX and curY != endY:
				curX = startX
				xIdx += 1
				curY = curY + cellSize
				yIdx = 0
				# Move to the next iteration of the loop
				continue
			elif curX == endX and curY == endY:
				break
			rectIdx += 1
			yIdx += 1

		self.canvas.pack(fill = BOTH, expand = 1)


	# Method to redraw the positions of the robots and the frontier
	def redraw(self, height, width, cellSize, grid, robots, frontier):

		self.parent.title('Grid2')
		self.pack(fill = BOTH, expand = 1)

		# canvas = Canvas(self.parent)

		self.canvas.delete('all')

		startX = cellSize
		startY = cellSize
		endX = startX + (cellSize * width)
		endY = startY + (cellSize * height)

		curX = startX
		curY = startY
		rectIdx = 0
		xIdx = 0
		yIdx = 0

		while curX != endX and curY != endY:
			
			# print 'x, y:', xIdx, yIdx
			# First, check if the current location corresponds to that of any robot
			robotFlag = False
			for robot in robots:
				if robot.curX == xIdx and robot.curY == yIdx:
					robotFlag = True
					self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = '#0000FF', fill = '#00FF00', width = 2)
			# Then check if it corresponds to an obstacle
			if grid.cells[xIdx][yIdx].obstacle == True:
				self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = '#0000FF', fill = '#000000', width = 2)	
			elif robotFlag == False:
				# Then check if it corresponds to a frontier cell
				frontierFlag = False
				for pt in frontier:
					if pt[0] == xIdx and pt[1] == yIdx:
						self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = '#0000FF', fill = '#00FFFF', width = 2)
						frontierFlag = True

				if frontierFlag == False:
					if grid.cells[xIdx][yIdx].visited == True:
						self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = '#0000FF', fill = '#FFFFFF', width = 2)
					else:
						self.canvas.create_rectangle(curX, curY, curX + cellSize, curY + cellSize, outline = '#0000FF', fill = '#777777', width = 2)
			
			curX = curX + cellSize
			if curX == endX and curY != endY:
				curX = startX
				xIdx += 1
				curY = curY + cellSize
				yIdx = 0
				# Move to the next iteration of the loop
				continue
			elif curX == endX and curY == endY:
				break
			rectIdx += 1
			yIdx += 1

		self.canvas.pack(fill = BOTH, expand = 1)