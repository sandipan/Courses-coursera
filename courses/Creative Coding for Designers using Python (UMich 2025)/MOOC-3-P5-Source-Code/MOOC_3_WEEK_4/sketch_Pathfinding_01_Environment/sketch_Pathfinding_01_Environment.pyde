import random  # Import the random module for generating random numbers.
from Environment import Environment  # Import the Environment class from a separate module.

canvas_width = 1200  # Define the canvas width.
canvas_height = 600  # Define the canvas height.

def setup():
    size(canvas_width, canvas_height)  # Initialize the canvas size.
    background(0)  # Set the canvas background color.
    
    global my_environment  # Declare my_environment as a global variable.
    # Initialize my_environment with specific parameters and canvas size.
    my_environment = Environment(120, 60, canvas_width, canvas_height)
    
def draw():
    background(0)  # Clear the canvas with a background color.
    
    my_environment.run()  # Execute the run method of my_environment instance.
