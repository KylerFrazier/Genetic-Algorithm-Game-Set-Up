import tkinter as tk
from tkinter import Tk, Frame, Canvas, Label, Button, Radiobutton, font
from time import sleep
from games import MovingBall
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class Controls(Frame):

    def __init__(self, master=None, cnf={}, **kw):
        
        super().__init__(master, cnf, **kw)

        self.color = "white"
        self.background = "gray15"
        self.button_background = "gray25"
        self.hover = "gray55"
        self.button_selected = "gray40"
        self.border = "gray"
        self.font_family = "Times New Roman"

        self.configure(
            background=self.background, 
            highlightbackground=self.border, 
            highlightthickness=5
        )

    def make_label(self, text="", size=14):

        temp_font = font.Font(family=self.font_family, size=size)
        label = Label(
            master=self, 
            foreground=self.color,
            background=self.background,
            font=temp_font,
            text=text,
        )
        label.grid(padx=50, pady=50)
        return label

    def make_radio_buttons(self, var=1, choices=[], size=14):
        temp_font = font.Font(family=self.font_family, size=size)
        radiobuttons = []
        for i, choice in enumerate(choices):
            rbutton = Radiobutton(
                master=self,
                text=choice,
                font=temp_font,
                foreground=self.color,
                background=self.button_background,
                activebackground=self.hover,
                activeforeground=self.color,
                selectcolor=self.button_selected,
                indicatoron=0,
                borderwidth=0,
                width=10,
                pady=10,
                variable=var,
                value=i
            )
            rbutton.grid(padx=10, pady=10)
            radiobuttons.append(rbutton)
        return radiobuttons

    def make_button(self, text="", function=lambda : None, size=14, ):

        temp_font = font.Font(family=self.font_family, size=size)
        button = Button(
            master=self,
            foreground=self.color,
            background=self.button_background,
            activebackground=self.hover,
            activeforeground=self.color,
            font=temp_font,
            text=text,
            pady=25,
            padx=25,
            borderwidth=0
        )
        button.grid(padx=50, pady=50)
        button.bind("<Button-1>", lambda _, *args, **kwargs : function(*args, **kwargs ))
        return button

    
class UserInterface(Tk):

    def __init__(self):
        
        super().__init__()

        self.title("Brick Breaker Menu")
        self.configure(background="black")
        
        self.controls = Controls(master=self)

        self.choice = tk.IntVar()
        self.choice.set(0)

        self.controls.title = self.controls.make_label(
            "Brick Breaker AI Controls", 20)
        self.controls.choice_buttons = self.controls.make_radio_buttons(
            self.choice, ["User", "A.I."])
        self.controls.gen = self.controls.make_button(
            "Generate Game", self.gen_game)


        self.controls.pack(fill=tk.Y, side=tk.LEFT)

        self.game_frame = Frame()
        self.game_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        self.game_frame.configure(background="gray15")
        
        self.random_seed = 0
        self.games = []
        
        self.mainloop()

    def gen_game(self):

        if len(self.games) != 0:
            for game in self.games:
                game.destroy()
        
        self.games = []
        if self.choice.get() == 0:
            self.games.append(MovingBall(self.game_frame))
            self.games[0].pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        else:
            rows=5
            col=8
            for i in range(rows):
                for j in range(col):
                    self.games.append(MovingBall(self.game_frame, width=300, height=300))
                    self.games[i*col+j].grid(row=i, column=j)
        
        self.update()
        
        for game in self.games:
            game.generate(self.random_seed)

        if self.choice.get() == 0:
            self.games[0].bind_keys()
        else:
            self.games[0].bind_keys()
            # REPLACE THIS WITH BINDING TO A.I.
        
        self.random_seed += 1
