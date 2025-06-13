"""
Description.
"""

import random  # Import the random module for potential random operations.
from Environment import Environment  # Import the Environment class to create and manage the simulation environment.

# Define the dimensions for the drawing canvas.
canvas_width = 1200
canvas_height = 600

def setup():
    # Initialize the drawing environment with a specified size and set the initial background.
    size(canvas_width, canvas_height)  # Set the canvas size to the defined dimensions.
    background(0)  # Set the canvas background to black.
    
    global my_environment  # Declare a global variable for the environment instance.
    # Create an instance of Environment with specified dimensions.
    my_environment = Environment(120, 60, canvas_width, canvas_height)
    
    
def draw():
    # This function runs continuously to update the display window.
    background(0)  # Clear the canvas with a black background each frame.
    my_environment.run()  # Update and run the environment's logic.
    
    # Check for mouse press interactions to modify the environment.
    if (mousePressed):
        if mouseButton == LEFT:
            # On left click, change the cell's type or perform an action like painting or selecting.
            my_environment.paint_cell(mouseX, mouseY, 1)  # Paint or modify the cell at the mouse position.
        if mouseButton == RIGHT:
            # On right click, reset or change the cell's type back to another state.
            my_environment.paint_cell(mouseX, mouseY, 0)  # Reset or modify the cell at the mouse position.
    
    # Check for key press interactions to control the simulation.
    if(keyPressed):
        if key == 's' or key == 'S':
            # If 's' or 'S' is pressed, start or resume the simulation logic.
            my_environment.running = True  # Set the running state of the environment to True.
