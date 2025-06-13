import random  # Import random module for potential use.
from Environment import Environment  # Import the Environment class to manage the simulation environment.

# Define the dimensions for the canvas.
canvas_width = 1200
canvas_height = 600

def setup():
    # Initialize the drawing environment with specified dimensions and set the initial background.
    size(canvas_width, canvas_height)  # Set the canvas size to the defined dimensions.
    background(0)  # Set the canvas background to black.
    
    global my_environment  # Declare a global variable for the environment instance.
    # Create an Environment object with specified grid dimensions and canvas size.
    my_environment = Environment(30, 15, canvas_width, canvas_height)
    
def draw():
    # Continuously update the canvas and the environment.
    background(0)  # Clear the canvas with a black background each frame.
    my_environment.run()  # Call the run method of the environment to update and display its state.
