"""
In this file model initiation takes place (init function). Then, in the 'step' function,
is everything that should occur every timestep. Events at every timestep are now:
- ants move one step in a random direction of the Moore neighborhood
"""
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from .agent import Ant, Brood

import random

WIDTH = 20
HEIGHT = 20

class Anthill(Model):
    def __init__(self):
        self.num_ants = 25
        self.num_brood = 5
        self.grid = MultiGrid(WIDTH, HEIGHT, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.ids = [i for i in range(self.num_ants)]

        # Create ants all at initiation
        # for i in range(self.num_agents):
        #     a = Ant(i, self)
        #     self.schedule.add(a)
        #     # Add the agent to a random grid cell
        #     x = self.random.randrange(self.grid.width)
        #     y = self.random.randrange(self.grid.height)
        #     self.grid.place_agent(a, (x, y))

        for i in range(self.num_brood):
            b = Brood(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(b, (x, y))

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        # Create one agent every timestep
        if len(self.ids) != 0:
            a = Ant(self.ids.pop(), self)
            self.schedule.add(a)
            x = int((WIDTH - 1) / 2)
            y = HEIGHT - 1
            self.grid.place_agent(a, (x, y))
