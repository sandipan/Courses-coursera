import random
from Particle import Particle
from Force import Force
from Vector_Field import Vector_Field

canvas_size_x = 1200  # Set canvas width
canvas_size_y = 600   # Set canvas height

all_particles = []  # List to store particles
all_forces = []  # List to store forces

def setup():
    size(canvas_size_x, canvas_size_y)  # Initialize the canvas with specified dimensions
    
    background(0)  # Set the canvas background to black
    
    global my_field  # Declare my_field globally for use in draw()
    # Initialize vector field with the specified number of columns, rows, and canvas dimensions
    my_field = Vector_Field(80, 40, canvas_size_x, canvas_size_y)
    # The call to initiate the vector field is commented out; it should be enabled to populate the field
    
def draw():
    background(0)  # Clear the canvas for each frame
    smooth()  # Apply smoothing for better visual quality
    my_field.run()  # Update and display the vector field
    
    fill(255,0,0)  # Set fill color to red for highlighting
    noStroke()  # Disable stroke for highlight drawing
    
    # Get force at mouse location and highlight it
    highlighted = my_field.get_force(mouseX, mouseY)
    # Display the highlighted force vector with specified size
    highlighted.display_highlight(10)
    
    # Particle updating and display are commented out; enable to include particle simulation
    #for p in all_particles:
    #    p.run()
