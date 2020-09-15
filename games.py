import tkinter as tk
from tkinter import Tk, TclError, Frame, Canvas, Label, font

class GameCanvas(Canvas):

    def __init__(self, master=None, cnf={}, width=852, height=480, **kw):
        
        kw["width"] = width
        kw["height"] = height
        super().__init__(master, cnf, **kw)

        self.configure(
            background="gray15", 
            highlightbackground="blue", 
            highlightthickness=5
        )

        self.update_frame_time()

    def vw(self, percentage):

        return percentage*self.winfo_width()/100

    def vh(self, percentage):

        return percentage*self.winfo_height()/100
    def update_frame_time(self, fps = 25):

        self.frame_time = int(1000/fps)
        return self.frame_time

    def animate(self):

        try:
            self.update()
        except TclError:
            exit(0)
        
        self.after(self.frame_time, self.animate)


class MovingBall(GameCanvas):

    def __init__(self, master=None, cnf={}, width=852, height=480, **kw):
        
        super().__init__(master, cnf, width, height, **kw)
        vw, vh = width/100, height/100
        self.ball = self.create_oval(
            50*vw - 10, 50*vh - 10, 50*vw + 10, 50*vh + 10, 
            fill = "white", tag = "animate"
        )
        
        self.dx, self.dy = 0, 0
        self.speed = 15
        self.pressed = {
            'up' : False, 
            'left' : False, 
            'down' : False, 
            'right' : False
        }

        self.after(0, self.animate)


    def bind_keys(self):
        
        self.master.bind("<KeyPress-w>", lambda _ : self.up(True))
        self.master.bind("<KeyPress-a>", lambda _ : self.left(True))
        self.master.bind("<KeyPress-s>", lambda _ : self.down(True))
        self.master.bind("<KeyPress-d>", lambda _ : self.right(True))
        self.master.bind("<KeyRelease-w>", lambda _ : self.up(False))
        self.master.bind("<KeyRelease-a>", lambda _ : self.left(False))
        self.master.bind("<KeyRelease-s>", lambda _ : self.down(False))
        self.master.bind("<KeyRelease-d>", lambda _ : self.right(False))
        
    def up(self, press=True):

        self.pressed['up'] = press
        self.update_direction()

    def left(self, press=True):

        self.pressed['left'] = press
        self.update_direction()

    def down(self, press=True):

        self.pressed['down'] = press
        self.update_direction()

    def right(self, press=True):

        self.pressed['right'] = press
        self.update_direction()
    
    def update_direction(self):

        if self.pressed['up'] == self.pressed['down']:
            self.dy = 0
        elif self.pressed['up']:
            self.dy = -10
        else:
            self.dy = 10
        
        if self.pressed['left'] == self.pressed['right']:
            self.dx = 0
        elif self.pressed['left']:
            self.dx = -10
        else:
            self.dx = 10


    def update(self):
        
        # if end_condition:
        #     self.gui.destroy()
        
        self.move(self.ball, self.dx, self.dy)
