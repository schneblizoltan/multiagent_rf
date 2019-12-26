import sys

from utils.ConfigFileReader import ConfigFileReader
from gui.GridUI import GridUI
from tkinter import Tk, Canvas, Frame, BOTH
from math import floor

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
root = Tk()
# gui = GridUI.GridUI(root, height, width, cellSize, algo.gridworld, algo.robots, algo.frontier)