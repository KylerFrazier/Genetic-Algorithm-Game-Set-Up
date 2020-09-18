import tkinter as tk
from abc import ABCMeta, abstractmethod

class GameCanvas(tk.Canvas, metaclass=ABCMeta):

    def __init__(self, master=None, cnf={}, width=1280, height=720, fps=25, **kw):
        
        kw["width"] = width
        kw["height"] = height
        super().__init__(master, cnf, **kw)

        self.configure(
            background="gray15",
            highlightbackground="green",
            highlightthickness=5
        )

        self.set_fps(fps)
        self.score = None

    @abstractmethod
    def generate(self):

        pass

    @abstractmethod
    def get_bindings(self) -> dict:
        
        return {}

    @abstractmethod
    def get_state(self) -> dict:

        return {}

    @abstractmethod
    def update(self):

        return 0

    def get_score(self):

        return self.score

    def vw(self, percentage=1):

        return percentage*self.winfo_width()/100

    def vh(self, percentage=1):

        return percentage*self.winfo_height()/100
    
    def set_fps(self, fps=25):

        self.fps = fps
        self.frame_time = 0 if fps == 0 else int(1000/fps)
        return self.frame_time
    
    def get_fps(self):

        return self.fps

    def get_actions(self) -> list:
        bindings = self.get_bindings()
        return [bindings[binding] for binding in sorted(bindings)]

    def bind_keys(self, bind=True):
        
        for binding, action in self.get_bindings().items():
            if bind:
                self.winfo_toplevel().bind(binding, action)
            else:
                self.winfo_toplevel().unbind(binding)

    def animate(self):

        try:
            score = self.update()
        except tk.TclError:
            self.destroy()
        
        if score == None:
            self.after(self.frame_time, self.animate)
        else:
            self.bind_keys(False)
            self.destroy()
            self.score = score
            return score
