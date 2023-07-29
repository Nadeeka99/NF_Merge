import turtle
import random

# Set up the turtle
screen = turtle.Screen()
screen.bgcolor("white")
turtle.speed(0)

# List of colors
colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]

# Function to draw a random shape
def draw_shape(size):
    for _ in range(random.randint(3, 10)):
        turtle.forward(size)
        turtle.left(360 / random.randint(3, 10))

# Main art loop
for _ in range(36):  # You can adjust the number of repetitions to change the complexity of the art
    color = random.choice(colors)
    turtle.pencolor(color)
    turtle.fillcolor(color)

    turtle.begin_fill()
    draw_shape(random.randint(30, 100))
    turtle.end_fill()

    turtle.right(10)  # Adjust the angle to change the orientation of the shapes

# Hide the turtle and display the art
turtle.hideturtle()
turtle.done()
