from math import sqrt
from random import seed, random as rand
from collections import namedtuple
from utils.game_canvas import GameCanvas
from utils.vectors import Vector2D

# Move the ball to the goal by accelerating it. The Ball has air resistance
# and momentum. Controlled with the WASD keys; press CTRL to run.
class MovingBall(GameCanvas):

    def generate(self):
        
        seed(self.random_seed)
        
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

        self.min_dist = self.vw(100) + self.vh(100)
        self.tics = 0
        self.score_factor = 1/self.distance(self.r, self.goal_r)

        self.after(0, self.animate)
    
    def get_actions(self) -> list:

        return [self.up, self.left, self.down, self.right, self.run]

    def get_bindings(self) -> dict:
        
        return {
            "<KeyPress-w>" : (lambda _=None : self.up(True)),
            "<KeyPress-a>" : (lambda _=None : self.left(True)),
            "<KeyPress-s>" : (lambda _=None : self.down(True)),
            "<KeyPress-d>" : (lambda _=None : self.right(True)),
            "<KeyPress-Control_L>" : (lambda _=None : self.run(True)),
            "<KeyPress-Up>" : (lambda _=None : self.up(True)),
            "<KeyPress-Left>" : (lambda _=None : self.left(True)),
            "<KeyPress-Down>" : (lambda _=None : self.down(True)),
            "<KeyPress-Right>" : (lambda _=None : self.right(True)),
            "<KeyPress-Control_R>" : (lambda _=None : self.run(True)),
            "<KeyRelease-w>" : (lambda _=None : self.up(False)),
            "<KeyRelease-a>" : (lambda _=None : self.left(False)),
            "<KeyRelease-s>" : (lambda _=None : self.down(False)),
            "<KeyRelease-d>" : (lambda _=None : self.right(False)),
            "<KeyRelease-Control_L>" : (lambda _=None : self.run(False)),
            "<KeyRelease-Up>" : (lambda _=None : self.up(False)),
            "<KeyRelease-Left>" : (lambda _=None : self.left(False)),
            "<KeyRelease-Down>" : (lambda _=None : self.down(False)),
            "<KeyRelease-Right>" : (lambda _=None : self.right(False)),
            "<KeyRelease-Control_R>" : (lambda _=None : self.run(False))
        }

    def get_state(self) -> list:
        
        return [self.r.x - self.goal_r.x, self.r.y - self.goal_r.y]

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
        
        self.dist = self.distance(self.r, self.goal_r)
        self.min_dist = min(self.min_dist, self.dist)
        if self.tics >= 100:
            return -self.min_dist
        if self.dist <= abs(self.R - self.goal_R):
            return 1 / (self.tics+1)
        
        self.tics += 1

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

class Pong(GameCanvas):

    def generate(self):

        seed(self.random_seed)

        self.vm = self.vw if self.vw() < self.vh() else self.vh
        self.dim = (self.vw, self.vh)
        self.score = 0
        
        # Paddle / Agent
        self.height = self.vh(10)
        self.width = self.vw(2)
        self.x = 2 * self.width
        self.y = self.vh(50)
        self.dy = self.vh(2)
        self.paddle = self.create_rectangle(
            self.x-self.width,
            self.y-self.height/2,
            self.x,
            self.y+self.height/2,
            fill="white"
        )

        # Wall / Unbeatable Advisary
        self.wall_x = self.vw(100) - self.x
        self.wall = self.create_rectangle(
            self.wall_x,
            -self.vh(100),
            self.wall_x + self.width,
            self.vh(200),
            fill="white"
        )


        # Ball
        self.R = self.vh(1)
        self.r = Vector2D(self.vw(49), self.vh(50))
        self.v = Vector2D(-self.vw(2), self.vw(2) * (2*rand() - 1))
        self.ball = self.create_oval(
            self.r.x - self.R, self.r.y - self.R, 
            self.r.x + self.R, self.r.y + self.R, 
            fill = "light blue"
        )

        self.pressed = {
            'up' : False, 
            'down' : False, 
        }

        self.after(0, self.animate)

    def get_actions(self) -> list:

        return [self.up, self.down]

    def get_bindings(self) -> dict:
        
        return {
            "<KeyPress-w>" : (lambda _=None : self.up(True)),
            "<KeyPress-s>" : (lambda _=None : self.down(True)),
            "<KeyPress-Up>" : (lambda _=None : self.up(True)),
            "<KeyPress-Down>" : (lambda _=None : self.down(True)),
            "<KeyRelease-w>" : (lambda _=None : self.up(False)),
            "<KeyRelease-s>" : (lambda _=None : self.down(False)),
            "<KeyRelease-Up>" : (lambda _=None : self.up(False)),
            "<KeyRelease-Down>" : (lambda _=None : self.down(False)),
        }

    def get_state(self) -> list:
        
        return [
            self.y - self.height/2, 
            self.vw(100) - (self.y - self.height/2), 
            self.r.x - self.R - self.x, 
            self.r.y - self.R - self.y
        ]
    
    def update(self):
        
        if self.r.x < 0:
            return self.score

        # Move Paddle and check wall collisions
        if self.pressed['up'] and not self.pressed['down']:
            if self.y - self.dy < self.height/2:
                self.move_paddle(self.height/2 - self.y)
            else:
                self.move_paddle(-self.dy)
        elif self.pressed['down'] and not self.pressed['up']:
            if self.y + self.dy > self.vh(100) - self.height/2:
                self.move_paddle(self.vh(100) - self.height/2 - self.y)
            else:
                self.move_paddle(self.dy)
        
        ball_d = Vector2D(*self.v)

        # Move ball and check paddle and wall collisions
        if (self.r.x - self.R + self.v.x < self.x
        and self.r.x - self.R > self.x
        and self.y-self.height/2 < self.r.y < self.y+self.height/2):
            self.v.x = -1*self.v.x
            self.v.y = abs(self.v.x) * (self.r.y - self.y) / (self.height/2)
            ball_d.x = self.v.x - (self.r.x - self.x)
            self.score += 1
        elif self.r.x + self.R + self.v.x > self.wall_x:
            self.v.x = -1*self.v.x 
            self.v.y = abs(self.v.x) * (2*rand() - 1)
            ball_d.x = self.v.x - (self.r.x - self.wall_x)
        
        # Move ball and check ceiling and floor collisions
        if self.r.y - self.R + self.v.y < 0:
            self.v.y = -1*self.v.y
            ball_d.y = self.v.y - self.r.y
        elif self.r.y + self.R + self.v.y > self.vh(100):
            self.v.y = -1*self.v.y
            ball_d.y = self.v.y - (self.r.y - self.vh(100))
        
        self.move_ball(*ball_d)
        
    def move_paddle(self, dy):

        self.y += dy
        self.move(self.paddle, 0, dy)
    
    def move_ball(self, dx, dy):
        
        self.r.x += dx
        self.r.y += dy
        self.move(self.ball, dx, dy)
    
    def up(self, press=True):

        # if press != self.pressed['up']:
        #     self.score += 0.1
        self.pressed['up'] = press
        
    def down(self, press=True):

        # if press != self.pressed['down']:
        #     self.score += 0.1
        self.pressed['down'] = press

