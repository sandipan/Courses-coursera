import random
from Particle import Particle
from Force import Force
from Vector_Field import Vector_Field

canvas_size_x = 1200  # Canvas width
canvas_size_y = 600   # Canvas height

all_particles = []  # List to store particles
all_forces = []  # List to store forces

mouse_history = []  # List to track mouse position history

def setup():
    size(canvas_size_x, canvas_size_y)  # Initialize canvas
    background(0)  # Set background color
    
    global my_field  # Declare vector field globally
    my_field = Vector_Field(80, 40, canvas_size_x, canvas_size_y)  # Initialize vector field

def draw():
    background(0)  # Clear canvas
    smooth()  # Apply smoothing
    my_field.run()  # Update and display vector field
    
    fill(255, 0, 0)  # Set fill color for highlighting
    noStroke()  # Disable stroke
    
    highlighted = my_field.get_force(mouseX, mouseY)  # Get force vector under mouse
    
    my_field.all_forces[highlighted].display_highlight(10)  # Highlight the selected force vector
    
    mouse_vector = calc_mouse_history()  # Calculate mouse movement vector
    
    my_field.add_force(highlighted, mouse_vector)  # Add or set the force vector based on mouse movement

def calc_mouse_history():
    mouse_history.append(PVector(mouseX, mouseY))  # Append current mouse position
    
    if len(mouse_history) > 2:  # Keep history length to 2
        mouse_history.pop(0)  # Remove oldest entry
    
    if len(mouse_history) > 1:  # If there are enough points to calculate a vector
        stroke(255)  # Set stroke color
        # Draw a line between the two most recent points
        line(mouse_history[0].x, mouse_history[0].y,
             mouse_history[1].x, mouse_history[1].y)
        
        mouse_vector = mouse_history[1].copy().sub(mouse_history[0])  # Calculate vector from mouse movement
        return mouse_vector  # Return the calculated mouse vector
    else:
        return PVector(0, 0)  # Return a zero vector if not enough history
