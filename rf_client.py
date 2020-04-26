import sys

from utils.ConfigFileReader import ConfigFileReader
from gui import GridUI, Cell, Grid
from tkinter import Tk, Canvas, Frame, BOTH
from math import floor
from agents.q_agent import QAgent
from agents.Agent import Agent
from environment.environment import Environment

def readConfigFile(fileName):
    cfr = ConfigFileReader()

    ret, height, width, numRobots, initLocs, obstacles = cfr.readConfigFile("config_files/barmaze.config")
    if ret == -1: 
        print('readCfg() Unsuccessful!')
        sys.exit(-1)
    
    printConfigValues(height, width, numRobots, initLocs, obstacles)
    return height, width, numRobots, initLocs, obstacles

def printConfigValues(height, width, numRobots, initLocs, obstacles):
    print('height =', height)
    print('width =', width)
    print('numRobots =', numRobots)
    print('initLocs =', initLocs)
    print('obstacles =', obstacles)

def initGridWorld(gridworld, agents, initLocs):
    i = 0
    for initLoc in initLocs:
        agents[i].setLocation(initLoc[0], initLoc[1])
        gridworld.cells[initLoc[0]][initLoc[1]].occupied = True
        gridworld.cells[initLoc[0]][initLoc[1]].visited = True
        i = i + 1

def main():
    height, width, numRobots, initLocs, obstacles = readConfigFile("config_files/barmaze.config")

    maxScreenHeight = 700
    cellSize = int(floor(maxScreenHeight / (height + 2)))

    gridworld = Grid.Grid(width, height, obstacles)
    env = Environment(height, width, gridworld)
    agents = [QAgent(j+1, -1, -1, env.state_n, env.action_n) for j in range(numRobots)]
    env.agents = agents

    initGridWorld(gridworld, agents, initLocs)
    print(env.printGrid())

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

if __name__ == '__main__':
	main()