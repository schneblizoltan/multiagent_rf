class Agent:

	def __init__(self, id, curX, curY):
		self.id = id
		self.curX = curX
		self.curY = curY

	def setLocation(self, curX, curY):
		self.curX = curX
		self.curY = curY