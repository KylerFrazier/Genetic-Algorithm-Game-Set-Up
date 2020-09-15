import tkinter as tk
from tkinter import Tk, TclError, Frame, Canvas, Label, font
from vectors import Vector2D
from math import sqrt

class GameCanvas(Canvas):

    def __init__(self, master=None, cnf={}, width=0, height=0, fps=25, **kw):
        
        if width == 0 or height == 0:
            width = master.winfo_screenwidth() - master.winfo_width()
            height = master.winfo_screenheight()
            master.state("zoomed")
        
        kw["width"] = width
        kw["height"] = height
        super().__init__(master, cnf, **kw)

        self.configure(
            background="gray15", 
            highlightbackground="blue", 
            highlightthickness=5
        )

        self.update_frame_time(fps)

    def vw(self, percentage=1):

        return percentage*self.winfo_width()/100

    def vh(self, percentage=1):

        return percentage*self.winfo_height()/100
    
    def update_frame_time(self, fps = 25):

        self.frame_time = 0 if fps == 0 else int(1000/fps)
        return self.frame_time

    def animate(self):

        if self.frame_time != 0:
            try:
                self.update()
            except TclError:
                exit(0)
        
        self.after(self.frame_time, self.animate)


# Move the ball by accelerating it. The Ball has air resistance and momentum.

class MovingBall(GameCanvas):

    def __init__(self, master=None, cnf={}, width=0, height=0, fps=25, **kw):
        
        super().__init__(master, cnf, width, height, fps, **kw)

    def generate(self):
        self.vm = self.vw if self.vw() < self.vh() else self.vh
        
        self.a = Vector2D(0,0)
        self.v = Vector2D(0,0)
        self.r = Vector2D(self.vw(50), self.vh(50))
        self.R = self.vm(3)
        self.max_a = self.vm(0.2)
        self.air_k = 0.01

        self.pressed = {
            'up' : False, 
            'left' : False, 
            'down' : False, 
            'right' : False
        }

        self.ball = self.create_oval(
            self.r.x - self.R, self.r.y - self.R, 
            self.r.x + self.R, self.r.y + self.R, 
            fill = "white"
        )

        self.after(0, self.animate)

    def update_acceleration(self):
        
        # Air resistance
        
        for i in range(len(self.v)):
            sign = -1 if self.v[i] > 0 else 1
            self.v[i] += sign * self.air_k * (self.v[i])**2#, abs(self.v[i]))
            if abs(self.v[i]) < self.vm(0.1):
                self.v[i] = 0

        # Keyboard press

        if self.pressed['up'] == self.pressed['down']:
            self.a.y = 0
        elif self.pressed['up']:
            self.a.y = -1
        else:
            self.a.y = 1
        
        if self.pressed['left'] == self.pressed['right']:
            self.a.x = 0
        elif self.pressed['left']:
            self.a.x = -1
        else:
            self.a.x = 1
            
        a_scale = 0 if self.a.x == 0 and self.a.y == 0 else \
            self.max_a / sqrt(self.a.x**2 + self.a.y**2)
        self.a.x *= a_scale
        self.a.y *= a_scale

        self.v.x += self.a.x
        self.v.y += self.a.y

    def update(self):
        
        # if end_condition:
        #     self.destroy()

        self.update_acceleration()
        self.move(self.ball, self.v.x, self.v.y)

    def bind_keys(self):
        
        self.master.bind("<KeyPress-w>", lambda _ : self.up(True))
        self.master.bind("<KeyPress-a>", lambda _ : self.left(True))
        self.master.bind("<KeyPress-s>", lambda _ : self.down(True))
        self.master.bind("<KeyPress-d>", lambda _ : self.right(True))
        self.master.bind("<KeyPress-Up>", lambda _ : self.up(True))
        self.master.bind("<KeyPress-Left>", lambda _ : self.left(True))
        self.master.bind("<KeyPress-Down>", lambda _ : self.down(True))
        self.master.bind("<KeyPress-Right>", lambda _ : self.right(True))
        self.master.bind("<KeyPress-Control_L>", lambda _ : self.run(True))
        self.master.bind("<KeyRelease-w>", lambda _ : self.up(False))
        self.master.bind("<KeyRelease-a>", lambda _ : self.left(False))
        self.master.bind("<KeyRelease-s>", lambda _ : self.down(False))
        self.master.bind("<KeyRelease-d>", lambda _ : self.right(False))
        self.master.bind("<KeyRelease-Up>", lambda _ : self.up(False))
        self.master.bind("<KeyRelease-Left>", lambda _ : self.left(False))
        self.master.bind("<KeyRelease-Down>", lambda _ : self.down(False))
        self.master.bind("<KeyRelease-Right>", lambda _ : self.right(False))
        self.master.bind("<KeyRelease-Control_L>", lambda _ : self.run(False))
        
    def up(self, press=True):

        self.pressed['up'] = press

    def left(self, press=True):

        self.pressed['left'] = press

    def down(self, press=True):

        self.pressed['down'] = press

    def right(self, press=True):

        self.pressed['right'] = press

    def run(self, press=True):

        self.max_a = self.vm(1) if press else self.vm(0.2)
        