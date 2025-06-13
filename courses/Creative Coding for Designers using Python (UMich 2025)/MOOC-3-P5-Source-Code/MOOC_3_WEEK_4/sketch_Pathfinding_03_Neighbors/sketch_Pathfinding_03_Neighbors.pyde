import random  # Import the random module for potential use.
from Environment import Environment  # Import the Environment class for the simulation.

canvas_width = 1200  # Set the canvas width.
canvas_height = 600  # Set the canvas height.

def setup():
    size(canvas_width, canvas_height)  # Initialize the canvas size.
    background(0)  # Set the initial background color to black.
    
    global my_environment  # Declare a global variable for the environment.
    # Create an instance of Environment with specific dimensions.
    my_environment = Environment(120, 60, canvas_width, canvas_height)
    
    
def draw():
    background(0)  # Clear the canvas with a black background at each draw call.
    my_environment.run()  # Update the environment at each frame.

    # Check if the mouse is pressed to interact with the canvas.
    if (mousePressed):
        if mouseButton == LEFT:
            # If the left mouse button is pressed, highlight the cell and its neighbors.
            my_environment.draw_neighbors(mouseX, mouseY)
        if mouseButton == RIGHT:
            # If the right mouse button is pressed, change the cell type at mouse position.
            my_environment.paint_cell(mouseX, mouseY, 2)
