from turtle import Turtle, Screen
import math

# Create a turtle instance
t = Turtle()

# Parameters for the circle
radius = 100
circumference = 2 * math.pi * radius
num_steps = 360  # Number of steps to approximate the circle
step_length = circumference / num_steps
angle = 360 / num_steps

# Draw the circle
for _ in range(num_steps):
    t.forward(step_length)
    t.left(angle)

# Keep the window open until it is closed by the user
screen = Screen()
screen.mainloop()
