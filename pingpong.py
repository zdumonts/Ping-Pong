from tkinter import *
import time
import random

class Ball:
    def __init__(self, canvas, color, size, paddle, ai_paddle):
        self.canvas = canvas
        self.paddle = paddle
        self.ai_paddle = ai_paddle
        self.id = canvas.create_oval(10, 10, size, size, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.xspeed = random.randrange(-2,2)
        self.yspeed = -1
        self.hit_bottom = False
        self.score = 0

    def draw(self):
        self.canvas.move(self.id, self.xspeed, self.yspeed)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.yspeed = 3
        if pos[3] >= 400:
            self.hit_bottom = True
        if pos[0] <= 0:
            self.xspeed = 3
        if pos[2] >= 500:
            self.xspeed = -3
        if self.hit_paddle(pos, self.paddle) == True:
            self.yspeed = -3
            self.xspeed = random.randrange(-2,2)
            self.score += 1
        if self.hit_paddle(pos, self.ai_paddle) == True:
            self.yspeed = 3
            self.xspeed = random.randrange(-2,2)

    def hit_paddle(self, pos, paddle):
        paddle_pos = self.canvas.coords(paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

class Paddle:
    def __init__(self, canvas, color, is_ai=False):
        self.canvas = canvas
        self.is_ai = is_ai
        self.id = canvas.create_rectangle(0,0, 100, 10, fill=color)
        if self.is_ai:
            self.canvas.move(self.id, 200, 50)
        else:
            self.canvas.move(self.id, 200, 300)
            self.xspeed = 0
            self.canvas.bind_all('<a>', self.move_left)
            self.canvas.bind_all('<d>', self.move_right)

    def draw(self):
        if not self.is_ai:
            self.canvas.move(self.id, self.xspeed, 0)
            pos = self.canvas.coords(self.id)
            if pos[0] <= 0:
                self.xspeed = 0
            if pos[2] >= 500:
                self.xspeed = 0
        else:
            ball_pos = self.canvas.coords(ball.id)
            paddle_pos = self.canvas.coords(self.id)
            self.canvas.move(self.id, ball_pos[0]-paddle_pos[0]-50, 0)

    def move_left(self, evt):
        self.xspeed = -3
    def move_right(self, evt):
        self.xspeed = 3

tk = Tk()
tk.title("Ball Game")
canvas = Canvas(tk, width=500, height=400, bd=0, bg='white')
canvas.pack()
label = canvas.create_text(5, 5, anchor=NW, text="Score: 0")
tk.update()
paddle = Paddle(canvas, 'black')
ai_paddle = Paddle(canvas, 'black', True)
ball = Ball(canvas, 'black', 25, paddle, ai_paddle)

while ball.hit_bottom == False:
    ball.draw()
    paddle.draw()
    ai_paddle.draw()
    canvas.itemconfig(label, text="Score: "+str(ball.score))
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)

go_label = canvas.create_text(250,200,text="GAME OVER",font=("Times",30))
tk.update() 