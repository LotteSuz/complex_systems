"""
Here are all the different types of agents.
Ants: move randomly
Brood: don't do anything but exist
Fence:Boundarary
"""
from mesa import Agent
import numpy as np

# ---> This is a bit messy here, but needed to calculate bound_vals 
# for list of boundary coordinates, wasn't sure where else to put it
WIDTH = 20
HEIGHT = 20
bound_vals=[]
brood_init=[]
ants_init=[]
for i in range(WIDTH):
    for j in range(HEIGHT):
        if i == 2 and 2 <= j <= HEIGHT - 3:
            bound_vals.append((i, j))
        elif i == WIDTH - 3 and 2 <= j <= HEIGHT - 3:
            bound_vals.append((i, j))
        elif 3 <= i <= WIDTH - 4 and j == 2:  ##aviod overlap
            bound_vals.append((i, j))
        elif 3 <= i <= WIDTH - 4 and j == HEIGHT - 3:  ##aviod overlap
            bound_vals.append((i, j))
        elif 2 < i < WIDTH - 3 and 2 < j < HEIGHT - 3:
            brood_init.append((i, j))
        else:
            ants_init.append((i, j))


class Ant(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)


    def force_calc(self):
        """ Calculate the force acting on the ant. """

        ##check the neighbor if it is Ant

        # Calculate the force in x and y direction 
        Fx = 0
        if type(self.model.grid[self.pos[0]-1][self.pos[1]]) is Ant:
            Fx += 1
        if type(self.model.grid[self.pos[0]+1][self.pos[1]]) is Ant:
            Fx -= 1

        Fy = 0 
        if type(self.model.grid[self.pos[0]][self.pos[1]-1]) is Ant:
            Fy += 1
        if type(self.model.grid[self.pos[0]][self.pos[1]+1]) is Ant:
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
        ## check if the ants can go into the internal
        if self.pos in ants_init:
            if self.random.uniform(0, 1) > 0.5:
                new_position = self.random.choice(brood_init)
                if self.model.grid.is_cell_empty(new_position) == True:
                    self.model.grid.move_agent(self, new_position)
        else:
            Fx, Fy, F = self.force_calc()
            if F == 0:
                # When there are no neighbors, move into any neighbor
                possible_steps = self.model.grid.get_neighborhood(self.pos,moore=False,include_center=False)
                new_position = self.random.choice(possible_steps)
                if self.model.grid.is_cell_empty(new_position) == True:
                    self.model.grid.move_agent(self, new_position)
                ## if the next position is boundary, then go back to the ants initial place

                elif type(self.model.grid[new_position[0]][new_position[1]]) is Fence:
                    new_position = self.random.choice(ants_init)
                    if self.model.grid.is_cell_empty(new_position) == True:
                        self.model.grid.move_agent(self, new_position)

            else:
                # Calculate the new preferred direction, rounding to nearest integer
                c = (int(round(Fx / F)), int(round(Fy / F)))
                new_position = (self.pos[0] + c[0], self.pos[1] + c[1])

                    # ant if it has moved onto the boundary and it will go back to the area
                if type(self.model.grid[new_position[0]][new_position[1]]) is Fence:
                    new_position = self.random.choice(ants_init)
                    if self.model.grid.is_cell_empty(new_position) == True:
                        self.model.grid.move_agent(self, new_position)
                elif self.model.grid.is_cell_empty(new_position):
                    self.model.grid.move_agent(self, new_position)


    def step(self):
        self.move()

class Brood(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)


class Fence(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)

