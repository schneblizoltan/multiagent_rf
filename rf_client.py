import sys

from utils.ConfigFileReader import ConfigFileReader
from gui import GridUI, Cell, Grid
from tkinter import Tk, Canvas, Frame
from math import floor
from agents.q_agent import QAgent
from agents.Agent import Agent
from environment.environment import Environment

MAX_SCREEN_HEIGHT = 700

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

def initGridWorld(width, height, obstacles, initLocs, numRobots):
    gridworld = Grid.Grid(width, height, obstacles)
    env = Environment(height, width, gridworld)
    agents = [QAgent(j, -1, -1, env.state_n, env.action_n) for j in range(numRobots)]

    i = 0
    for initLoc in initLocs:
        agents[i].setLocation(initLoc[0], initLoc[1])
        gridworld.cells[initLoc[0]][initLoc[1]].occupied = True
        gridworld.cells[initLoc[0]][initLoc[1]].visited = True
        i = i + 1

    env.agents = agents
    env.updateFrontiers()
    print(env.printGrid())

    return env

def main():
    height, width, numRobots, initLocs, obstacles = readConfigFile("config_files/barmaze.config")

    cellSize = int(floor(MAX_SCREEN_HEIGHT / (height + 2)))
    
    env = initGridWorld(width, height, obstacles, initLocs, numRobots)

    root = Tk()
    gui = GridUI.GridUI(root, height, width, cellSize, env.gridworld, env.agents, env.frontier)

    def run():
        env.runOneIter()
        gui.redraw(height, width, cellSize, env.gridworld, env.agents, env.frontier)
        root.after(50, run)

    root.after(50, run)
    root.mainloop()

if __name__ == '__main__':
	main()