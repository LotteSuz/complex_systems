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
        self.internalrate = 0.2
        self.ant_id = 1

        # List containing all coordinates of the boundary, initial ants location and brood location
        self.bound_vals = []
        self.ants_init = []
        self.brood_init = []
        self.neigh_bound = []

        for i in range(WIDTH):
            for j in range(HEIGHT):
                if i == 0 or j == 0 or i == WIDTH-1 or j == HEIGHT-1:
                    self.bound_vals.append((i,j))
                elif i == 1 or i == WIDTH - 2 or j == 1 or j == HEIGHT-2:
                    self.neigh_bound.append((i,j))

                # if i == 2 and 2 <= j <= HEIGHT - 3:
                #     self.bound_vals.append((i, j))
                # elif i == WIDTH - 3 and 2 <= j <= HEIGHT - 3:
                #     self.bound_vals.append((i, j))
                # elif 3 <= i <= WIDTH - 4 and j == 2:  ##aviod overlap
                #     self.bound_vals.append((i, j))
                # elif 3 <= i <= WIDTH - 4 and j == HEIGHT - 3:  ##aviod overlap
                #     self.bound_vals.append((i, j))
                # elif 2 < i < WIDTH - 3 and 2 < j < HEIGHT - 3:
                #     self.brood_init.append((i, j))
                # else:
                #     self.ants_init.append((i, j))

                # if i == 4 or i == WIDTH - 4 or j == 4 or j == HEIGHT-4:
                #     self.neigh_bound.append((i,j))

                # for i in range(1,WIDTH-1):
                #     for j in range(1,HEIGHT-1):
                #         if i == 1 or i == WIDTH-2 or j ==1 or j == (HEIGHT-2):
                #             bound_vals.append((i,j))


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

        # for i in range(self.num_brood):
        #     while True:
        #         x = random.randint(3,WIDTH-3)
        #         y = random.randint(3, HEIGHT - 3)

        #         if self.grid.is_cell_empty((x,  y)) == True:
        #             fe = Brood(i, self)
        #             self.grid.place_agent(fe, (x, y))
        #             break
        #         else:
        #             continue


    def step(self):
        '''Advance the model by one step.'''

        # Add new ants into the internal area ont he boundary
        for xy in self.neigh_bound:

            # Add with probability internal rate and if the cell is empty
            if self.random.uniform(0, 1) < self.internalrate and self.grid.is_cell_empty(xy) == True:

                a = Ant(self.ant_id, self)

                self.schedule.add(a)
                self.grid.place_agent(a,xy)

                self.ant_id += 1

        # Move the ants
        self.schedule.step()
