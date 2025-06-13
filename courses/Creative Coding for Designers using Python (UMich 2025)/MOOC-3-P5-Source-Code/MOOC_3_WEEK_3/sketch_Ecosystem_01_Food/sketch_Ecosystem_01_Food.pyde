import random  # Import random module for generating random numbers (if needed within World_Manager)
from World_Manager import World_Manager  # Import the World_Manager class

# Canvas dimensions are set globally for easy reference and modification
canvas_width = 1200
canvas_height = 600

# Initialize an instance of World_Manager with the defined canvas dimensions
my_world = World_Manager(canvas_width, canvas_height)

def setup():
    # Initialize the Processing canvas with specified dimensions
    size(canvas_width, canvas_height)
    background(0)  # Set the canvas background to black
    
    
def draw():
    global my_world  # Ensure the 'my_world' instance is accessible within the draw function
    background(0)  # Clear the canvas with a black background for each frame
    
    my_world.run()  # Call the 'run' method of the 'World_Manager' instance to update and render the world state
