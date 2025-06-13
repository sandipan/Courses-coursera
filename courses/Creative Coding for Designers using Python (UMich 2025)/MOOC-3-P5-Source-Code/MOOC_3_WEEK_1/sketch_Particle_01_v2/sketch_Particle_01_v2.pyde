import random
from Particle import Particle  # Import the Particle class

# Canvas dimensions
canvas_size_x = 1200  # Width of the canvas
canvas_size_y = 600   # Height of the canvas

all_particles = []  # List to store all particle instances

def setup():
    # Initialize the canvas
    size(canvas_size_x, canvas_size_y)  # Set the size of the canvas
    background(0)  # Set the background color to black
    
    # Create 100 Particle instances at a fixed position
    for i in range(100):
        x = 600  # Fixed x-coordinate for all particles
        y = 300  # Fixed y-coordinate for all particles
        # Initialize a new Particle instance with a position vector and canvas dimensions
        new_particle = Particle(PVector(x, y), canvas_size_x, canvas_size_y)
        all_particles.append(new_particle)  # Add the new Particle to the list of all particles
    
def draw():
    background(0)  # Clear the canvas with a black background at the start of each draw cycle
    
    # Iterate through all particles and update their state
    for p in all_particles:
        p.run()  # Call the run method of each Particle instance
