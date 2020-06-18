"""
In this file model initiation takes place (init function). Then, in the 'step' function,
is everything that should occur every timestep. Events at every timestep are now:
- ants move one step in a random direction of the Moore neighborhood
"""
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from .agent import Ant, Brood,Fence

import numpy as np

WIDTH = 25
HEIGHT = 25


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
        self.tau = np.zeros((WIDTH,HEIGHT))
        self.datacollector = DataCollector({"Total number of Ants": lambda m: self.get_total_ants_number(),
                                            "mean tau": lambda m: self.evaluation1(),
                                            "sigma": lambda m: self.evaluation2(),
                                            "sigma*" :  lambda m: self.evaluation3(),
                                            })


        # List containing all coordinates of the boundary, initial ants location and brood location
        self.bound_vals = []
        self.ants_init = []
        self.brood_init = []
        self.neigh_bound = []
        self.datacollector.collect(self)

        for i in range(WIDTH):
            for j in range(HEIGHT):
                if i == 0 or j == 0 or i == WIDTH-1 or j == HEIGHT-1:
                    self.bound_vals.append((i,j))
                if i == 1 or i == WIDTH - 2 or j == 1 or j == HEIGHT-2:
                    self.neigh_bound.append((i,j))
                if 0<i<WIDTH - 1 and 0<j<HEIGHT-1:
                    self.brood_init.append((i,j))




        # Make a Fence boundary
        b = 0
        for h in self.bound_vals:
            br = Fence(b,self)
            # self.schedule.add(br)
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
        self.datacollector.collect(self)

    def get_total_ants_number(self):
        total_ants=0
        for (agents, _, _) in self.grid.coord_iter():
            if type(agents) is Ant:
                total_ants += 1
        return total_ants

    def evaluation1(self):
        ##creat a empty grid to store currently information
        total_ants = np.zeros((WIDTH,HEIGHT))

        ## count the number of currently information
        for (agents, i, j) in self.grid.coord_iter():
            if type(agents) is Ant:
                total_ants[i][j] = 1
            else:
                total_ants[i][j] = 0
        ##update the tau
        self.tau = self.tau + total_ants
        ##calcualte the mean tau
        self.mean_tau_ant = self.tau.sum()/((WIDTH-2)**2)
        return self.mean_tau_ant

    def evaluation2(self):


        ## we need to minus the mean tau so we need to ensure the result of boundary is zero
        ## so we let the bounday equal mean_tau_ant in this way the (tau-mean_tau_ant) is zero of boundary
        for site in self.bound_vals:
            self.tau[site[0]][site[1]] = self.mean_tau_ant


        ##calculate the sigmaa
        self.sigma = ((self.tau-self.mean_tau_ant)**2).sum()/((WIDTH-2)**2)

        ## rechange the boundaryy
        for site in self.bound_vals:
            self.tau[site[0]][site[1]] = 0

        return np.sqrt(self.sigma)

    def evaluation3(self):
        ##calculate the sigmastar
        sigmastar = np.sqrt(self.sigma)/self.mean_tau_ant

        return sigmastar















