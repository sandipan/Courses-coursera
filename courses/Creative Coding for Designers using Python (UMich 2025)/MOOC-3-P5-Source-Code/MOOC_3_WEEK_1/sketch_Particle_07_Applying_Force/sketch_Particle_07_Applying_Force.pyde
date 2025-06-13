import random
from Particle import Particle
from Force import Force

# Canvas dimensions
canvas_size_x = 1200
canvas_size_y = 600

all_particles = []  # List to store particles
all_forces = []  # List to store forces

def setup():
    # Initializes canvas and creates forces and particles
    size(canvas_size_x, canvas_size_y)  # Set canvas size
    background(0)  # Set background color to black
    smooth()  # Enable smooth drawing for better visuals
    
    # Create forces and add them to the forces list
    new_force = Force(PVector(200,200), PVector(-20,60))  # First force
    all_forces.append(new_force)  # Add to list
    new_force_2 = Force(PVector(1000,400), PVector(10,-40))  # Second force
    all_forces.append(new_force_2)  # Add to list
    
    # Create 200 particles and add them to the particles list
    for i in range(200):
        x = 600  # X coordinate
        y = 300  # Y coordinate
        # Instantiate a new particle and add it to the list
        new_particle = Particle(pos = PVector(x, y),
                                world_x = canvas_size_x, 
                                world_y = canvas_size_y, 
                                part_list = all_particles, 
                                force_list = all_forces
                                )
        all_particles.append(new_particle)  # Add to particles list
    
def draw():
    # Animation loop: clears canvas and updates particles and forces
    background(0)  # Clear canvas
    
    # Update and draw all particles
    for p in all_particles:
        p.run()  # Particle behavior
    
    # Update and draw all forces
    for f in all_forces:
        f.run()  # Force behavior
