import random
from Particle import Particle

# Canvas dimensions
canvas_size_x = 1200
canvas_size_y = 600

all_particles = []  # List to store particle instances

def setup():
    # Initialize canvas and particles
    size(canvas_size_x, canvas_size_y)  # Set canvas size
    background(0)  # Set background color to black
    smooth()  # Enable smooth edges
    
    # Create 100 Particle instances at a fixed position
    for i in range(100):
        x = 600  # X position
        y = 300  # Y position
        # Create and add new particle to the list
        new_particle = Particle(PVector(x, y), canvas_size_x, canvas_size_y, all_particles)
        all_particles.append(new_particle)
    
def draw():
    background(0)  # Clear the screen for each frame
    
    # Run each particle's behavior
    for p in all_particles:
        p.run()
