import random
from Particle import Particle
from Force import Force
from Vector_Field import Vector_Field

canvas_size_x = 1200  # Define canvas width
canvas_size_y = 600   # Define canvas height

all_particles = []  # List to hold particle objects
all_forces = []  # List to hold force objects

mouse_history = []  # Track mouse position history

def setup():
    size(canvas_size_x, canvas_size_y)  # Initialize canvas with specified dimensions
    background(0)  # Set background color to black
    
    global my_field  # Declare vector field globally
    my_field = Vector_Field(80, 40, canvas_size_x, canvas_size_y)  # Initialize vector field

def draw():
    background(0)  # Clear canvas
    smooth()  # Apply smoothing for better visuals
    my_field.run()  # Update and display vector field
    
    fill(255, 0, 0)  # Set fill color for highlighting
    noStroke()  # Disable stroke
    
    # Highlight and manipulate a single vector based on mouse position
    highlighted = my_field.get_force(mouseX, mouseY)  # Get index of force vector under mouse
    my_field.all_forces[highlighted].display_highlight(10)  # Highlight the selected vector
    
    # Calculate mouse movement vector
    mouse_vector = calc_mouse_history()
    
    # Highlight and manipulate adjacent vectors based on mouse position
    adjacent_vectors = my_field.get_adjacent_vectors(mouseX, mouseY)  # Get indices of adjacent vectors
    for i in adjacent_vectors:
        my_field.all_forces[i].display_highlight(10)  # Highlight adjacent vectors
        my_field.add_force(i, mouse_vector)  # Add mouse movement vector to adjacent forces

def calc_mouse_history():
    mouse_history.append(PVector(mouseX, mouseY))  # Append current mouse position
    
    if len(mouse_history) > 2:
        mouse_history.pop(0)  # Keep history to two entries for drawing line
    
    if len(mouse_history) > 1:
        stroke(255)  # Set stroke color for line
        # Draw line based on mouse history
        line(mouse_history[0].x, mouse_history[0].y,
             mouse_history[1].x, mouse_history[1].y)
        
        # Calculate and return vector based on mouse movement
        mouse_vector = mouse_history[1].copy().sub(mouse_history[0])
        return mouse_vector
    else:
        return PVector(0, 0)  # Return zero vector if not enough history
