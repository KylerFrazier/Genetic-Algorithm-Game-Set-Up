from random import choice, random as rand
from utils.agent_template import Agent

class RandomAgent(Agent):

    def act(self):

        if 100*rand() < 5:
            action = choice(self.actions)
            action(choice([True, False]))

class NeuralNetworkAgent(Agent):

    def __init__(self, problem, network, master=None, cnf={}, tps=25, **kw):

        super().__init__(problem, master, cnf, tps, **kw)
        self.network = network
    
    def act(self):

        output = self.network.activate(self.problem.get_state())
        for i, confidence in enumerate(output):
            if confidence > 0.5:
                self.actions[i](True)
            else:
                self.actions[i](False)

