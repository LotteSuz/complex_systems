"""
This file contains everything regarding the visualization and the server which
runs the model.
"""
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from .model import Anthill
from .agent import Ant, Brood

# IMPORTANT: the WIDTH and HEIGHT parameters are also in model.py; make sure
# to change those as well if you want to adjust the grid size
WIDTH = 20
HEIGHT = 20

def agent_portrayal(agent):
    if type(agent) is Brood:
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "black",
                     "r": 0.2}

    ## use this portrayal for dot visuals for the ant agents
    # portrayal = {"Shape": "circle",
    #              "Filled": "true",
    #              "Layer": 0,
    #              "Color": "black",
    #              "r": 0.2}

    ## use this portrayal for ant visuals
    if type(agent) is Ant:
        portrayal = {"Shape":"ant.jpg", "Layer":0}

    return portrayal

grid = CanvasGrid(agent_portrayal, WIDTH, HEIGHT)
server = ModularServer(Anthill,
                       [grid],
                       "Anthill")
server.port = 8521 # The default
