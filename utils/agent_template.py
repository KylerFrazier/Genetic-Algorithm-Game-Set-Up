import tkinter as tk
from time import sleep
from abc import ABCMeta, abstractmethod

class Agent(tk.Frame, metaclass=ABCMeta):

    def __init__(self, problem, master=None, cnf={}, tps=25, **kw):
        
        super().__init__(master, cnf, **kw)

        self.problem = problem
        self.actions = self.problem.get_actions()
        self.set_tps(self.problem.get_fps() if tps == None else tps)
        self.score = None

    @abstractmethod
    def act(self):

        pass
    
    def get_score(self):
        return self.score

    def start(self):

        self.after(0, self.run)

    def set_tps(self, tps=25):

        self.tps = tps
        self.tic_time = 0 if tps == 0 else int(100/tps)
        return self.tic_time

    def run(self):
        
        if not self.problem.winfo_exists():
            self.score = self.problem.get_score()
            self.destroy()
            return self.score
        
        self.state = self.problem.get_state()
        self.act()
        
        self.after(self.tic_time, self.run)
