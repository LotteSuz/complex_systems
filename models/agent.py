"""
Here are all the different types of agents.
Ants: move randomly
Brood: don't do anything but exist
"""
from mesa import Agent
import numpy as np

# ---> This is a bit messy here, but needed to calculate bound_vals 
# for list of boundary coordinates, wasn't sure where else to put it
WIDTH = 20
HEIGHT = 20
bound_vals = []
for i in range(1,WIDTH-1):
    for j in range(1,HEIGHT-1):
        if i == 1 or i == WIDTH-2 or j ==1 or j == (HEIGHT-2):
            bound_vals.append((i,j))


class Ant(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def force_calc(self):
        """ Calculate the force acting on the ant. """

        # Make a list of possible steps for each ant
        possible_steps = self.model.grid.get_neighbors(
            self.pos,
            moore=False,
            include_center=False)

        possible_steps = [a.pos for a in possible_steps]

        # print('possible_steps',possible_steps,self.pos)

        # Calculate the force in x and y direction 
        Fx = 0
        if (self.pos[0]-1,self.pos[1]) in possible_steps:
            Fx += 1
        if (self.pos[0]+1,self.pos[1]) in possible_steps:
            Fx -= 1

        Fy = 0 
        if (self.pos[0],self.pos[1]-1) in possible_steps:
            Fy += 1
        if (self.pos[0],self.pos[1]+1) in possible_steps:
            Fy -= 1

        # Magnitude of the force
        F = np.sqrt(Fx**2+Fy**2)

        return Fx,Fy,F

    def stoch_move(self,c):
        """ Moves are selected stochastically """
        # First find possible trial configurations
        trials = []
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                # Skip the centre and the preferered direction c
                if (x!=0 or y !=0):
 
                    if self.model.grid.is_cell_empty((self.pos[0] + x,self.pos[1] + y)) == True:
                        trials.append((x,y))
        w = []
        beta = 1
        for i in trials:
            # The magnitude of vector difference c and c*
            d = np.sqrt((i[0] - c[0])**2 + (i[1] - c[1])**2)
            w.append(np.exp(-beta * d))
        sumw = np.sum(w)

        # Select one with probability w/sumw
        n = self.select(sumw,w)

        return trials[n]

    def select(self,sumw,w):
        """ Select one of the trial configurations,c*, with probability eq. 11. """

        ws = self.random.uniform(0,1) * sumw
        cumw = w[0]
        n = 0
        while(cumw < ws):
            n += 1
            cumw += w[n]

        return n

    def move(self):
        if self.pos:

            Fx,Fy,F = self.force_calc()

            if F == 0:
                # When there are no neighbors, don't move
                c = (0,0)
            else:

                # Calculate the new preferred direction, rounding to nearest integer
                c = (int(round(Fx/F)), int(round(Fy/F)))

            # ---> Comment out next line for stochastic thingy
            # c = self.stoch_move(c)
            
            new_position = (self.pos[0]+c[0], self.pos[1] + c[1])
            # print('New position',new_position)

            # Only move if the new cell is empty
            if self.model.grid.is_cell_empty(new_position):
                self.model.grid.move_agent(self, new_position)

                # Remove ant if it has moved onto the boundary
                if new_position in bound_vals:
                    self.model.grid.remove_agent(self)

        else:
            
            # Place a new ant with a probability
            if self.random.uniform(0, 1) > 0.5:

                # Generate random coordinate on the boundary (that doesn't contain ant)
                xy = self.random.choice(bound_vals)
                while self.model.grid.is_cell_empty(xy) == False:
                    xy = self.random.choice(bound_vals)
                self.model.grid.place_agent(self, xy)

    def step(self):
        self.move()

class Brood(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)

