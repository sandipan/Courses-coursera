import random  # Import the random module for potential randomization within the environment.
from Environment import Environment  # Import the Environment class to manage the simulation.

# Define the canvas dimensions.
canvas_width = 1200
canvas_height = 600

count = 0  # Initialize a counter to manage the progression of simulation steps.
t_count = 0  # Initialize a target count to control the pace of the simulation.

def setup():
    # Initialize the drawing environment with specified dimensions and set the initial background.
    size(canvas_width, canvas_height)  # Set the canvas size to the defined dimensions.
    background(0)  # Set the canvas background to black.
    
    global my_environment
    # Create an Environment object with specified grid dimensions and canvas size.
    my_environment = Environment(30, 15, canvas_width, canvas_height)
    
def draw():
    # The draw function is called in a loop to update the display window.
    global count, t_count
    if count < t_count:
        my_environment.run()  # Update and run the environment's logic.
        count += 1  # Increment the counter after each run to control the simulation pace.

def keyReleased():
    # Function to handle key release events.
    global t_count
    t_count += 1  # Increment the target count each time a key is released to advance the simulation.
