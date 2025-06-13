import random
from Particle import Particle
from Force import Force

# Canvas dimensions
canvas_size_x = 1200
canvas_size_y = 600

all_particles = []  # List to store particle instances
all_forces = []  # List to store force instances

def setup():
    # Initialize canvas with specified dimensions and initial settings
    size(canvas_size_x, canvas_size_y)  # Set canvas size
    background(0)  # Set background color to black
    smooth()  # Enable smooth drawing
    
    # Create force instances and add them to the force list
    new_force = Force(PVector(200,200), PVector(-20,60))  # First force
    all_forces.append(new_force)  # Add to forces list
    new_force_2 = Force(PVector(1000,400), PVector(10,-40))  # Second force
    all_forces.append(new_force_2)  # Add to forces list
    
    # Create particle instances and add them to the particle list
    for i in range(100):
        x = 600  # Fixed X position for particles
        y = 300  # Fixed Y position for particles
        # Create new particle with specified position, canvas bounds, and reference lists
        new_particle = Particle(pos = PVector(x, y),
                                world_x = canvas_size_x, 
                                world_y = canvas_size_y, 
                                part_list = all_particles, 
                                force_list = all_forces
                                )
        all_particles.append(new_particle)  # Add to particles list
    
def draw():
    # Update canvas and entities each frame
    background(0)  # Clear canvas
    
    # Update and draw particles
    for p in all_particles:
        p.run()  # Execute particle behavior
    
    # Update and draw forces
    for f in all_forces:
        f.run()  # Execute force behavior
