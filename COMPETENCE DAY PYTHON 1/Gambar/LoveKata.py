import turtle
from math import pi, sin, cos

def draw_heart(w, h, iteration=0):
    if iteration >= len(colors):
        return
    
    t = turtle.Turtle()
    t.hideturtle()
    t.pensize(2.5)
    a = 0
    t.up()
    t.fillcolor(colors[iteration])
    t.begin_fill()
    while a < 2 * pi:
        x = w * (16 * sin(a) ** 3)
        y = h * (13 * cos(a) - 5 * cos(2 * a) - 2 * cos(3 * a) - cos(4 * a))
        t.goto(x, y)
        a += 0.02
        t.down()
    t.end_fill()

    draw_heart(w - 3, h - 2, iteration + 1)

   
    if iteration == len(colors) - 1:  
        t.up()
        t.color("black")
        t.setpos(0, 0)
        t.write("kata kata nya", align="center", font=("verdana", 20, "bold"))
        t.down()

colors = ['red'] 


screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.bgcolor("white")
screen.title("lop lop")


draw_heart(16, 16)


turtle.done()