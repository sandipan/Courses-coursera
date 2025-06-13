import random  # Import the random module.
from Environment import Environment  # Import the Environment class for creating the simulation environment.

# Define the dimensions for the canvas.
canvas_width = 1200
canvas_height = 600

def setup():
    size(canvas_width, canvas_height)  # Initialize the canvas size with specified dimensions.
    background(0)  # Set the background color of the canvas to black.
    
    global my_environment  # Declare my_environment as a global variable.
    # Create an Environment object with specified parameters for dimensions and size.
    my_environment = Environment(60, 30, canvas_width, canvas_height)
    
    
def draw():
    background(0)  # Clear the canvas with a black background at each frame.
    my_environment.run()  # Run the environment update for each frame.
    
    # Check for mouse press actions to interact with the environment.
    if (mousePressed):
        if mouseButton == LEFT:
            # On left click, change the type of the cell under the cursor to 1.
            my_environment.paint_cell(mouseX, mouseY, 1)
        if mouseButton == RIGHT:
            # On right click, change the type of the cell under the cursor to 2.
            my_environment.paint_cell(mouseX, mouseY, 2)
    
    # Check if any key is pressed.
    if(keyPressed):
        if key == 's' or key == 'S':
            # If 's' or 'S' is pressed, set the running state of the environment to True.
            my_environment.running = True
