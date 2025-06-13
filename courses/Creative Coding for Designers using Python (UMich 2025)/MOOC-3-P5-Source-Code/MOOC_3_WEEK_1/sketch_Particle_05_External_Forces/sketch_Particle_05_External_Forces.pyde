import random
from Particle import Particle
from Force import Force

# Canvas dimensions
canvas_size_x = 1200
canvas_size_y = 600

all_particles = []  # List to store all particle objects

def setup():
    # Initialize the canvas and create particles
    size(canvas_size_x, canvas_size_y)  # Set canvas size
    background(0)  # Set background color to black
    smooth()  # Enable smooth drawing
    
    # Initialize forces with position and direction
    global new_force, new_force_2  # Declare forces as global to use outside setup
    new_force = Force(PVector(200,200), PVector(-20,60))  # Create first force
    new_force_2 = Force(PVector(1000,400), PVector(10,-40))  # Create second force
    
    # Create 100 Particle instances at specified position
    for i in range(100):
        x = 600  # Fixed X position
        y = 300  # Fixed Y position
        # Instantiate and add new particle to the list
        new_particle = Particle(PVector(x, y), canvas_size_x, canvas_size_y, all_particles)
        all_particles.append(new_particle)
    
def draw():
    # Update the canvas and particles each frame
    background(0)  # Clear the canvas
    
    # Run force behaviors
    new_force.run()  # Update and display first force
    new_force_2.run()  # Update and display second force
    
    # Update and display each particle
    for p in all_particles:
        p.run()  # Run particle behavior
