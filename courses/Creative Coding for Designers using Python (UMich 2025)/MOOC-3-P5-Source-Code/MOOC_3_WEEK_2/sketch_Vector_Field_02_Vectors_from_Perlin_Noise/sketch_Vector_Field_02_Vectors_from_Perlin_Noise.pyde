import random
from Particle import Particle
from Force import Force
from Vector_Field import Vector_Field

canvas_size_x = 1200  # Set canvas width
canvas_size_y = 600   # Set canvas height

all_particles = []  # List for particles
all_forces = []  # List for forces

def setup():
    size(canvas_size_x, canvas_size_y)  # Initialize canvas
    background(0)  # Set background color
    smooth()  # Smooth drawing
    
    global my_field  # Declare vector field globally
    my_field = Vector_Field(31, 21)  # Create vector field with dimensions
    my_field.initiate_vecfield()  # Initialize vector field
    
def draw():
    background(0)  # Clear canvas for drawing
    my_field.run()  # Update and display vector field
    
    # Particle update and display commented out
    #for p in all_particles:
    #    p.run()
