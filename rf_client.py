import sys

from utils.ConfigFileReader import ConfigFileReader
from gui import GridUI, Cell, Grid
from tkinter import Tk, Canvas, Frame, BOTH
from math import floor
from agents import Agent

def readConfigFile(fileName):
    cfr = ConfigFileReader()

    #function
    ret, height, width, numRobots, R, baseX, baseY, initLocs, obstacles = cfr.readConfigFile("config_files/barmaze.config")
    if ret == -1: 
        print('readCfg() Unsuccessful!')
        sys.exit(-1)
    
    return height, width, numRobots, R, baseX, baseY, initLocs, obstacles

height, width, numRobots, R, baseX, baseY, initLocs, obstacles = readConfigFile("config_files/barmaze.config")

print(height, width, numRobots, R, baseX, baseY, initLocs, obstacles)

maxScreenHeight = 700
cellSize = int(floor(maxScreenHeight / (height + 2)))

gridworld = Grid.Grid(width, height, obstacles)
agents = [Agent.Agent(j+1, -1, -1) for j in range(numRobots)]
i = 0
for initLoc in initLocs:
    agents[i].setLocation(initLoc[0], initLoc[1])
    gridworld.cells[initLoc[0]][initLoc[1]].occupied = True
    gridworld.cells[initLoc[0]][initLoc[1]].visited = True
    i = i + 1

cells = [[Cell.Cell(i, j) for j in range(width)] for i in range(height)]
for obstacle in obstacles:
	cells[obstacle[0]][obstacle[1]].obstacle = True

frontier = []
for i in range(height):
    for j in range(width):
        if gridworld.cells[i][j].visited == False and gridworld.cells[i][j].obstacle == False:
            point = (i, j)
            neighbors = gridworld.get8Neighbors(point)
            frontierFlag = False
            for nbhr in neighbors:
                if gridworld.cells[nbhr[0]][nbhr[1]].visited == True:
                    frontierFlag = True

            if frontierFlag == True:
                frontier.append((i, j))

root = Tk()
gui = GridUI.GridUI(root, height, width, cellSize, gridworld, agents, frontier)

root.mainloop()