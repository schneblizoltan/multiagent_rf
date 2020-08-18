import sys, time

from utils.ConfigFileReader import ConfigFileReader
from gui import GridUI, Cell, Grid
from tkinter import Tk, Canvas, Frame
from math import floor
from agents.q_agent import QAgent
from agents.sarsa_agent import SarsaAgent
from agents.Agent import Agent
from environment.environment import Environment

MAX_SCREEN_HEIGHT = 700
NR_OF_EPISODES = 10000

TIME_RESULT_FILE_NAME = "time_15k_sarsa_agent.txt"
DISCOVER_RESULT_FILE_NAME = "discover_15k_sarsa_agent.txt"

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
    agents = [SarsaAgent(j, -1, -1, env.state_n, env.action_n) for j in range(numRobots)]

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

def initEnvironment(env, obstacles, initLocs):
    agents = env.agents
    gridworld = Grid.Grid(env.gridworld.width, env.gridworld.height, obstacles)
    env.gridworld = gridworld
    i = 0
    for initLoc in initLocs:
        agents[i].setLocation(initLoc[0], initLoc[1])
        env.gridworld.cells[initLoc[0]][initLoc[1]].occupied = True
        env.gridworld.cells[initLoc[0]][initLoc[1]].visited = True
        i = i + 1

    env.agents = agents
    env.updateFrontiers()

def decreaseAgentsExplorationRate(env):
    for agent in env.agents:
        agent.update_eps()

def printElapsedTimeToFile(time):
    if time == 0:
        time = 15000
    with open(TIME_RESULT_FILE_NAME, 'a') as out:
        out.write(str(time) + '\n')
    
def printDiscoveredAreaPercentage(env):
    with open(DISCOVER_RESULT_FILE_NAME, 'a') as out:
        out.write(str(env.gridworld.getDiscoveredPercentage()) + '\n')    

def main():
    height, width, numRobots, initLocs, obstacles = readConfigFile("config_files/barmaze.config")

    cellSize = int(floor(MAX_SCREEN_HEIGHT / (height + 2)))
    
    env = initGridWorld(width, height, obstacles, initLocs, numRobots)

    root = Tk()
    gui = GridUI.GridUI(root, height, width, cellSize, env.gridworld, env.agents, env.frontier)

    currEpisode = 0
    ellapsedTime = 0

    def run(currEpisode, ellapsedTime):
        if env.isExplored() or ellapsedTime == 300:
            currEpisode += 1
            print(currEpisode, "/", NR_OF_EPISODES, " episode")
            printElapsedTimeToFile(ellapsedTime)
            printDiscoveredAreaPercentage(env)
            initEnvironment(env, obstacles, initLocs)
            decreaseAgentsExplorationRate(env)
            ellapsedTime = 0
            env.runOneIter()
            gui.redraw(height, width, cellSize, env.gridworld, env.agents, env.frontier)
            root.after(50, lambda : run(currEpisode, ellapsedTime))
        else:
            ellapsedTime += 1      
            env.runOneIter()
            gui.redraw(height, width, cellSize, env.gridworld, env.agents, env.frontier)
            root.after(50, lambda : run(currEpisode, ellapsedTime))

    root.after(50, lambda : run(currEpisode, ellapsedTime))
    root.mainloop()

if __name__ == '__main__':
	main()