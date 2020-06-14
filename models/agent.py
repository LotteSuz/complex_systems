"""
Here are all the different types of agents.
Ants: move randomly
Brood: don't do anything but exist
"""
from mesa import Agent

class Ant(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()

class Brood(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
