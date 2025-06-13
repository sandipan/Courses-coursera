import random  # Import the random module.
from Environment import Environment  # Import the Environment class.

canvas_width = 1200  # Define canvas width.
canvas_height = 600  # Define canvas height.

def setup():
    size(canvas_width, canvas_height)  # Initialize the canvas size.
    background(0)  # Set the background color.
    
    global my_environment  # Declare my_environment as a global variable.
    # Create an Environment object with specified parameters.
    my_environment = Environment(120, 60, canvas_width, canvas_height)
    
    
def draw():
    background(0)  # Clear the canvas with a background color.
    my_environment.run()  # Execute the run method of the Environment object.
    
    if (mousePressed):  # Check if the mouse is pressed.
        if mouseButton == LEFT:  # If the left mouse button is pressed.
            # Get the cell index under the mouse cursor.
            mouse_cell = my_environment.get_cell(mouseX, mouseY)
            # Paint the cell with type 1.
            my_environment.paint_cell(mouse_cell, 1)
        if mouseButton == RIGHT:  # If the right mouse button is pressed.
            # Get the cell index under the mouse cursor.
            mouse_cell = my_environment.get_cell(mouseX, mouseY)
            # Paint the cell with type 2.
            my_environment.paint_cell(mouse_cell, 2)
