import random
from Particle import Particle
from Force import Force
from Vector_Field import Vector_Field

canvas_size_x = 1200  # Set the width of the canvas
canvas_size_y = 600   # Set the height of the canvas

all_particles = []  # Initialize list to store particles
all_forces = []  # Initialize list to store forces

def setup():
    size(canvas_size_x, canvas_size_y)  # Initialize the canvas with specified dimensions
    
    background(0)  # Set the canvas background to black
    
    global my_field  # Declare my_field globally to be used outside setup
    # Initialize the vector field with specified column and row count, and canvas dimensions
    my_field = Vector_Field(120, 80, canvas_size_x, canvas_size_y)
    # The call to initiate_vecfield is commented out; if it's part of the Vector_Field class, it should be uncommented to populate the field
    
def draw():
    background(0)  # Clear the canvas at the beginning of each draw cycle
    smooth()  # Apply smoothing to reduce visual artifacts
    
    my_field.run()  # Update and display the vector field
    
    # Particle updating and drawing is commented out; to use particles, uncomment and ensure particles are added to all_particles list in setup or elsewhere
    #for p in all_particles:
    #    p.run()
