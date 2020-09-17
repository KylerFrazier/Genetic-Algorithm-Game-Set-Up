from math import sqrt
from random import seed, random as rand
from utils.game_canvas import GameCanvas
from utils.vectors import Vector2D

# Move the ball to the goal by accelerating it. The Ball has air resistance
# and momentum. Controlled with the WASD keys; press CTRL to run.
class MovingBall(GameCanvas):

    def __init__(self, master=None, cnf={}, width=1280, height=720, fps=25, **kw):
        
        super().__init__(master, cnf, width, height, fps, **kw)

    def generate(self, random_seed=None):
        
        seed(random_seed)
        
        self.vm = self.vw if self.vw() < self.vh() else self.vh
        self.dim = (self.vw, self.vh)
        
        self.a = Vector2D(0,0)
        self.v = Vector2D(0,0)
        self.r = Vector2D(self.vw(50), self.vh(50))
        self.r2 = Vector2D(self.vw(50), self.vh(50))    # same as r_prime

        self.R = self.vm(3)
        self.max_a = self.vm(0.2)
        self.air_k = 0.01

        self.pressed = {
            'up' : False, 
            'left' : False, 
            'down' : False, 
            'right' : False
        }

        self.goal_R = self.vm(1)
        self.goal_r = Vector2D(
            rand()*self.vw(98) + self.goal_R,
            rand()*self.vh(98) + self.goal_R,
        )

        self.goal = self.create_oval(
            self.goal_r.x - self.goal_R, self.goal_r.y - self.goal_R,
            self.goal_r.x + self.goal_R, self.goal_r.y + self.goal_R,
            fill = "yellow"
        )

        self.ball = self.create_oval(
            self.r.x - self.R, self.r.y - self.R, 
            self.r.x + self.R, self.r.y + self.R, 
            fill = "light blue"
        )

        self.score = 0
        self.score_decrement = 1/self.distance(self.r, self.goal_r)

        self.after(0, self.animate)
    
    def bindings(self):
        
        return {
            "<KeyPress-w>" : (lambda _ : self.up(True)),
            "<KeyPress-a>" : (lambda _ : self.left(True)),
            "<KeyPress-s>" : (lambda _ : self.down(True)),
            "<KeyPress-d>" : (lambda _ : self.right(True)),
            "<KeyPress-Up>" : (lambda _ : self.up(True)),
            "<KeyPress-Left>" : (lambda _ : self.left(True)),
            "<KeyPress-Down>" : (lambda _ : self.down(True)),
            "<KeyPress-Right>" : (lambda _ : self.right(True)),
            "<KeyPress-Control_L>" : (lambda _ : self.run(True)),
            "<KeyRelease-w>" : (lambda _ : self.up(False)),
            "<KeyRelease-a>" : (lambda _ : self.left(False)),
            "<KeyRelease-s>" : (lambda _ : self.down(False)),
            "<KeyRelease-d>" : (lambda _ : self.right(False)),
            "<KeyRelease-Up>" : (lambda _ : self.up(False)),
            "<KeyRelease-Left>" : (lambda _ : self.left(False)),
            "<KeyRelease-Down>" : (lambda _ : self.down(False)),
            "<KeyRelease-Right>" : (lambda _ : self.right(False)),
            "<KeyRelease-Control_L>" : (lambda _ : self.run(False))
        }
    
    def distance(self, v1, v2) -> float:

        return sqrt((v1.x-v2.x)**2 + (v1.y-v2.y)**2)

    def update_all_motion(self):
        
        # Air resistance
        
        for i in range(len(self.v)):
            sign = -1 if self.v[i] > 0 else 1
            self.v[i] += sign * self.air_k * (self.v[i])**2
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

        self.r2.x += self.v.x
        self.r2.y += self.v.y

    def check_collision(self):
        
        for i in range(len(self.r)):
            if self.r2[i] - self.R < 0:
                self.r2[i] = self.R
                self.v[i] = 0
            if self.r2[i] + self.R > self.dim[i](100):
                self.r2[i] = self.dim[i](100) - self.R
                self.v[i] = 0

    def update(self):
        
        if self.distance(self.r, self.goal_r) <= abs(self.R - self.goal_R):
            return self.score
        
        self.score -= self.score_decrement

        self.update_all_motion()
        self.check_collision()
        self.move(
            self.ball, 
            self.r2.x - self.r.x, 
            self.r2.y - self.r.y
        )
        
        for i in range(len(self.r)):
            self.r[i] = self.r2[i]
        
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
        