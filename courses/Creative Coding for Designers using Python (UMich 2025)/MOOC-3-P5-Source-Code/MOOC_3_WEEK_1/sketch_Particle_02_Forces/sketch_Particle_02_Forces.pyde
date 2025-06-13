import random
from Particle import Particle  # Import the Particle class

# Define canvas dimensions
canvas_size_x = 1200  # Width of the canvas
canvas_size_y = 600   # Height of the canvas

all_particles = []  # Initialize an empty list to store all particle instances

def setup():
    # Create a canvas with the specified width and height
    size(canvas_size_x, canvas_size_y)
    
    # Set the background color of the canvas to black
    background(0)
    
    # Create 100 Particle instances with initial positions
    for i in range(100):
        x = 600  # Horizontal position 
        y = 300  # Vertical position 
        
        # Create a new Particle instance with the specified position and canvas dimensions
        new_particle = Particle(PVector(x, y), canvas_size_x, canvas_size_y)
        
        # Add the newly created particle to the list of all particles
        all_particles.append(new_particle)
    
def draw(): 
    # Clear the canvas with a black background at the beginning of each draw call
    background(0)
    
    # Iterate through the list of all particles
    for p in all_particles:
        # Call the run method of each particle, which is responsible for updating and displaying the particle
        p.run()
