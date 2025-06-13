import random
from Particle import Particle
from Force import Force
from Vector_Field import Vector_Field

canvas_size_x = 1200  # Set canvas width
canvas_size_y = 600   # Set canvas height

all_particles = []  # Initialize list for particles
all_forces = []  # Initialize list for forces

mouse_history = []  # Track mouse position history

def setup():
    size(canvas_size_x, canvas_size_y)  # Initialize canvas with specified dimensions
    background(0)  # Set background color to black
    
    global my_field  # Declare vector field globally
    my_field = Vector_Field(80, 40, canvas_size_x, canvas_size_y)  # Initialize vector field
    
def draw():
    background(0)  # Clear canvas every frame
    smooth()  # Apply smoothing for better visuals
    my_field.run()  # Update and display vector field
    
    fill(255,0,0)  # Set fill color to red for highlighting
    noStroke()  # Disable stroke for highlighted area
    
    highlighted = my_field.get_force(mouseX, mouseY)  # Get force vector under mouse
    highlighted.display_highlight(10)  # Highlight the selected force vector
    
    calc_mouse_history()  # Update and display mouse movement history
    
def calc_mouse_history():
    mouse_history.append(PVector(mouseX, mouseY))  # Append current mouse position to history
    
    if len(mouse_history) > 2:  # Limit history length to 2 for drawing a line
        mouse_history.pop(0)  # Remove oldest entry if exceeding limit
    
    if len(mouse_history) > 1:  # Check if there are enough points to draw a line
        stroke(255)  # Set line color to white
        # Draw a line connecting the two most recent mouse positions
        line(mouse_history[0].x, mouse_history[0].y,
             mouse_history[1].x, mouse_history[1].y)
    
    println(mouse_history)  # Print mouse history (for debugging)
