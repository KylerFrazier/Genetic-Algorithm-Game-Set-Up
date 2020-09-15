import tkinter as tk
from tkinter import Tk, Frame, Canvas, Label, font
from time import sleep
from games import MovingBall
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class Controls(Frame):

    def __init__(self, master=None, cnf={}, **kw):
        
        super().__init__(master, cnf, **kw)

        self.color = "white"
        self.background = "gray15"
        self.border = "gray"
        self.font_family = "Times New Roman"

        self.configure(
            background=self.background, 
            highlightbackground=self.border, 
            highlightthickness=5
        )

        self.title = self.make_label(20, "Brick Breaker AI Controls")
        self.temp = self.make_label(14, "temp")

    def make_label(self, size=14, text=""):
        temp_font = font.Font(family=self.font_family, size=size)
        label = Label(
            master=self, 
            foreground=self.color,
            background=self.background,
            font=temp_font,
            text=text
        )
        label.pack()
        return label

class UserInterface(Tk):

    def __init__(self):
        
        super().__init__()

        self.title("Brick Breaker Menu")
        self.configure(background="black")
        
        self.controls = Controls(master=self)
        self.controls.pack(fill=tk.Y, side=tk.LEFT)
        
        self.random_seed = 0
        self.generate_game()

        self.mainloop()

    def generate_game(self):

        self.game = MovingBall(self)
        self.game.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        self.update()
        
        self.game.generate(self.random_seed)
        self.game.bind_keys()

        self.random_seed += 1



    