import random
from Particle import Particle
from Force import Force
from Vector_Field import Vector_Field

canvas_size_x = 1200  # Set canvas width
canvas_size_y = 600   # Set canvas height

all_particles = []  # List to hold particle instances
all_forces = []  # Unused list intended to hold force instances

mouse_history = []  # List to track mouse positions over time

def setup():
    size(canvas_size_x, canvas_size_y)  # Initialize the canvas
    background(0)  # Set the background color to black
    
    global my_field  # Declare the vector field globally
    my_field = Vector_Field(80, 40, canvas_size_x, canvas_size_y)  # Initialize the vector field

def draw():
    background(0)  # Clear the canvas
    smooth()  # Apply smoothing to draw operations
    my_field.run()  # Display the vector field
    
    fill(255, 0, 0)  # Set fill color for highlighting
    noStroke()  # Disable stroke for drawing operations
    
    global highlighted, mouse_vector
    # Highlight a single vector under the mouse cursor
    highlighted = my_field.get_force(mouseX, mouseY)
    my_field.all_forces[highlighted].display_highlight(10)
    
    # Calculate mouse movement vector
    mouse_vector = calc_mouse_history()
    
    if mousePressed and mouseButton == LEFT:
        # Manipulate adjacent vectors when the mouse is pressed
        adjacent_vectors = my_field.get_adjacent_vectors(mouseX, mouseY, 4)  # Get vectors within 4 layers of adjacency
        for i in adjacent_vectors:
            my_field.all_forces[i].display_highlight(10)  # Highlight the adjacent vectors
            
            # Calculate directional vector from force to mouse
            diff = my_field.all_forces[i].pos.copy().sub(PVector(mouseX, mouseY))
            distance = diff.mag()  # Calculate distance from force to mouse
            
            factor = map(distance, 0, 100, 5.0, 0.0)  # Map distance to a scaling factor
            
            mouse_vector.normalize()  # Normalize mouse movement vector
            mouse_vector.mult(factor)  # Scale vector by calculated factor
            
            my_field.add_force(i, mouse_vector)  # Apply the modified vector to adjacent forces

def calc_mouse_history():
    mouse_history.append(PVector(mouseX, mouseY))  # Add current mouse position to history
    
    if len(mouse_history) > 2:
        mouse_history.pop(0)  # Ensure history only tracks the last two positions
    
    if len(mouse_history) > 1:
        stroke(255)  # Set stroke color to white
        # Draw a line representing mouse movement
        line(mouse_history[0].x, mouse_history[0].y,
             mouse_history[1].x, mouse_history[1].y)
        
        mouse_vector = mouse_history[1].copy().sub(mouse_history[0])  # Calculate movement vector
        return mouse_vector
    else:
        return PVector(0, 0)  # Return a zero vector if insufficient history
