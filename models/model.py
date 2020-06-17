"""
In this file model initiation takes place (init function). Then, in the 'step' function,
is everything that should occur every timestep. Events at every timestep are now:
- ants move one step in a random direction of the Moore neighborhood
"""
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid

from .agent import Ant, Brood,Fence

import random
import numpy as np

WIDTH = 20
HEIGHT = 20


class Anthill(Model):
    def __init__(self):
        self.num_ants = 25
        self.init_ants = 10
        self.num_brood = 10
        self.grid = SingleGrid(WIDTH, HEIGHT, False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.ids = [i for i in range(self.num_ants)]

        # List containing all coordinates of the boundary, initial ants location and brood location
        self.bound_vals = []
        self.ants_init = []
        self.brood_init = []

        for i in range(WIDTH):
            for j in range(HEIGHT):
                if i == 2 and 2 <= j <= HEIGHT - 3:
                    self.bound_vals.append((i, j))
                elif i == WIDTH - 3 and 2 <= j <= HEIGHT - 3:
                    self.bound_vals.append((i, j))
                elif 3 <= i <= WIDTH - 4 and j == 2:  ##aviod overlap
                    self.bound_vals.append((i, j))
                elif 3 <= i <= WIDTH - 4 and j == HEIGHT - 3:  ##aviod overlap
                    self.bound_vals.append((i, j))
                elif 2 < i < WIDTH - 3 and 2 < j < HEIGHT - 3:
                    self.brood_init.append((i, j))
                else:
                    self.ants_init.append((i, j))

        ##put the ants outside the boundary
        for i in range(self.num_ants):
            while True:
                antslocation = self.random.choice(self.ants_init)
                if self.grid.is_cell_empty((antslocation[0],  antslocation[1])) == True:
                    a = Ant(i, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (antslocation[0],  antslocation[1]))
                    break
                else:
                    continue

        # # Get initial coordinates for placing the ants
        # xy = self.random.sample(bound_vals,self.init_ants)
        #
        # # Put ants on the grid
        # for i in range(self.num_ants):
        #     a = Ant(i, self)
        #     self.schedule.add(a)
        #
        #     # First add only ten agents to random grid cell outside boundary
        #     if i < self.init_ants:
        #         self.grid.place_agent(a, xy[i])



        # Make a Fence boundary
        b = 0
        for h in self.bound_vals:
            br = Fence(b,self)
            self.grid.place_agent(br,(h[0],h[1]))
            b += 1

        ##Put Broods on the grid in the boundary

        # k=0
        # for i in brood_init:
        #     fe = Brood(k, self)
        #     self.grid.place_agent(fe, (i[0], i[1]))
        #     k+=1

        for i in range(self.num_brood):
            while True:
                x = random.randint(3,WIDTH-3)
                y = random.randint(3, HEIGHT - 3)

                if self.grid.is_cell_empty((x,  y)) == True:
                    fe = Brood(i, self)
                    self.grid.place_agent(fe, (x, y))
                    break
                else:
                    continue




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
