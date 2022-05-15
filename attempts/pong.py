# pong
import turtle
import random



# Load First Game Screen
win = turtle.Screen()
win.title("Pong")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)


# Score
score_A = 0
score_B = 0
score = 0

# Paddle A
paddle_A = turtle.Turtle()
paddle_A.speed(0)
paddle_A.shape("square")
paddle_A.color("white")
paddle_A.shapesize(stretch_wid=5, stretch_len=1)
paddle_A.penup()
paddle_A.goto(-350,0)

# Paddle B
paddle_B = turtle.Turtle()
paddle_B.speed(0)
paddle_B.shape("square")
paddle_B.color("white")
paddle_B.shapesize(stretch_wid=5, stretch_len=1)
paddle_B.penup()
paddle_B.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.1
ball.dy = -0.1

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"Player A: {score_A}     Player B: {score_B}", align="center", font=("Courier", 24, "normal"))


# Function
def paddle_A_up():
    y = paddle_A.ycor()
    y += 20
    paddle_A.sety(y)

def paddle_A_down():
    y = paddle_A.ycor()
    y -= 20
    paddle_A.sety(y)

def paddle_B_up():
    y = paddle_B.ycor()
    y += 20
    paddle_B.sety(y)

def paddle_B_down():
    y = paddle_B.ycor()
    y -= 20
    paddle_B.sety(y)

# Keyboard Binding
win.listen()
win.onkeypress(paddle_A_up, "w")
win.onkeypress(paddle_A_down, "s")
win.onkeypress(paddle_B_up, "Up")
win.onkeypress(paddle_B_down, "Down")


# Main game loop
while True:
    win.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)


    # Ball collisions with border and scoring
    if ball.ycor() >= 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() <= -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() >= 390:
        ball.goto(random.randrange(-60, 60), random.randrange(-50, 50))
        score_A += 1
        score += 1
        ball.dx = 0.1 * random.choice([-1, 1])
        ball.dy = 0.1 * random.choice([-1, 1])
        pen.clear()
        pen.write(f"Player A: {score_A}     Player B: {score_B}", align="center", font=("Courier", 24, "normal"))


    if ball.xcor() <= -390:
        ball.goto(random.randrange(-60, 60), random.randrange(-50, 50))
        score_B += 1
        score += 1
        ball.dx = 0.1 * random.choice([-1, 1])
        ball.dy = 0.1 * random.choice([-1, 1])
        pen.clear()
        pen.write(f"Player A: {score_A}     Player B: {score_B}", align="center", font=("Courier", 24, "normal"))


    # Ball collisions with paddle

    if -340 <= ball.xcor() <= -330 and paddle_A.ycor() - 55 <= ball.ycor() <= paddle_A.ycor() + 55:
        ball.setx(-330)
        ball.dx *= 1.1
        ball.dy *= 1.1
        ball.dx *= -1

    if 340 >= ball.xcor() >= 330 and paddle_B.ycor() - 55 <= ball.ycor() <= paddle_B.ycor() + 55:
        ball.setx(330)
        ball.dx *= 1.1
        ball.dy *= 1.1
        ball.dx *= -1

