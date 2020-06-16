"""
In this file model initiation takes place (init function). Then, in the 'step' function,
is everything that should occur every timestep. Events at every timestep are now:
- ants move one step in a random direction of the Moore neighborhood
"""
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid

from .agent import Ant, Brood

import random
import numpy as np

WIDTH = 20
HEIGHT = 20

# List containing all coordinates of the boundary
bound_vals = []
for i in range(1,WIDTH-1):
    for j in range(1,HEIGHT-1):
        if i == 1 or i == WIDTH-2 or j ==1 or j == (HEIGHT-2):
            bound_vals.append((i,j))

class Anthill(Model):
    def __init__(self):
        self.num_ants = 65
        self.init_ants = 10
        self.num_brood = 5
        self.grid = SingleGrid(WIDTH, HEIGHT, False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.ids = [i for i in range(self.num_ants)]

        # Get initial coordinates for placing the ants
        xy = self.random.sample(bound_vals,self.init_ants)

        # Put ants on the grid
        for i in range(self.num_ants):
            a = Ant(i, self)
            self.schedule.add(a)

            # First add only ten agents to random grid cell outside boundary
            if i < self.init_ants:
                self.grid.place_agent(a, xy[i])

        # Make a boundary of ants
        b=0
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if i % (WIDTH-1) == 0 or j % (HEIGHT-1) == 0:
                    
                    br = Brood(b,self)
                    self.grid.place_agent(br,(i,j))
                    b += 1

    def step(self):
        '''Advance the model by one step.'''

        self.schedule.step()

        # Create one agent every timestep
        # if len(self.ids) != 0:
        #     a = Ant(self.ids.pop(), self)

        #     self.schedule.add(a)
        #     x = int((WIDTH - 1) / 2)
        #     y = HEIGHT - 1
        #     self.grid.place_agent(a, (x, y))
