from random import choice, random as rand
from utils.agent_template import Agent

class RandomAgent(Agent):

    def act(self):

        if 100*rand() < 5:
            action = choice(self.actions)
            action()
