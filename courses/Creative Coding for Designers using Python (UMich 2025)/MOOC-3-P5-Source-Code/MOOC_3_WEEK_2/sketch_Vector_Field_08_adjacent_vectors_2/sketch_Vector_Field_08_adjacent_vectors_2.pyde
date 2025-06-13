import random
from Particle import Particle
from Force import Force
from Vector_Field import Vector_Field

canvas_size_x = 1200  # Define the canvas width
canvas_size_y = 600   # Define the canvas height

all_particles = []  # List to store all particle objects
all_forces = []  # List to store all force objects

mouse_history = []  # List to track the history of mouse positions

def setup():
    size(canvas_size_x, canvas_size_y)  # Initialize the canvas with specified dimensions
    background(0)  # Set the background color to black
    
    global my_field  # Declare the vector field globally
    my_field = Vector_Field(80, 40, canvas_size_x, canvas_size_y)  # Initialize the vector field

def draw():
    background(0)  # Clear the canvas
    smooth()  # Apply smoothing for better visual quality
    my_field.run()  # Execute the vector field's run method
    
    fill(255, 0, 0)  # Set the fill color to red
    noStroke()  # Disable drawing of strokes
    
    # Highlight a single vector based on the mouse position
    highlighted = my_field.get_force(mouseX, mouseY)  # Get the index of the force under the mouse
    my_field.all_forces[highlighted].display_highlight(10)  # Highlight this force vector
    
    # Calculate a vector based on the mouse's movement history
    mouse_vector = calc_mouse_history()
    
    # Highlight and manipulate adjacent vectors based on the mouse position
    # The function call to get_adjacent_vectors now incorrectly includes an additional argument '6'
    adjacent_vectors = my_field.get_adjacent_vectors(mouseX, mouseY, 6)  # This line is incorrect; the get_adjacent_vectors function expects two arguments, not three
    for i in adjacent_vectors:
        my_field.all_forces[i].display_highlight(10)  # Highlight adjacent vectors
        my_field.add_force(i, mouse_vector)  # Apply the mouse movement vector to adjacent forces

def calc_mouse_history():
    mouse_history.append(PVector(mouseX, mouseY))  # Add the current mouse position to the history
    
    if len(mouse_history) > 2:
        mouse_history.pop(0)  # Keep the history to the last two positions
    
    if len(mouse_history) > 1:
        stroke(255)  # Set the stroke color to white
        # Draw a line between the two most recent positions in the history
        line(mouse_history[0].x, mouse_history[0].y,
             mouse_history[1].x, mouse_history[1].y)
        
        # Calculate and return the vector representing the mouse's movement
        mouse_vector = mouse_history[1].copy().sub(mouse_history[0])
        return mouse_vector
    else:
        return PVector(0, 0)  # Return a zero vector if there's not enough history
