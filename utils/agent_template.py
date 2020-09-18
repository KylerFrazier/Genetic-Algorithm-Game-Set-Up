from time import sleep
from abc import ABCMeta, abstractmethod
from threading import Thread

class Agent(Thread, metaclass=ABCMeta):

    def __init__(self, problem, tps = None):
        
        super().__init__(daemon=True)

        self.problem = problem
        self.actions = self.problem.get_actions()
        self.set_tps(self.problem.get_fps() if tps == None else tps)
            
    @abstractmethod
    def act(self):

        pass

    def set_tps(self, tps=25):

        self.tic_time = 0 if tps == 0 else int(1/tps)
        return self.tic_time

    def run(self):
        
        while self.problem.winfo_exists():
            self.state = self.problem.get_state()
            self.act()
            sleep(self.tic_time)
        
        self.score = self.problem.get_score()
        return self.score
