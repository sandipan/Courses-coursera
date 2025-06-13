import random
from Particle import Particle
from Force import Force

canvas_size_x = 1200  # Set canvas width
canvas_size_y = 600   # Set canvas height

all_particles = []  # List for all particles
all_forces = []  # List for all forces

def setup():
    size(canvas_size_x, canvas_size_y)  # Initialize canvas
    background(0)  # Set background color
    smooth()  # Smooth edges
    
    # Create initial forces
    global new_force, new_force_2  # Define forces globally
    new_force = Force(PVector(200,200), PVector(-20,60))  # First force
    all_forces.append(new_force)  # Add to forces list
    new_force_2 = Force(PVector(1000,400), PVector(10,-40))  # Second force
    all_forces.append(new_force_2)  # Add to forces list
    
    # Create initial particles
    for i in range(100):
        x, y = 600, 300  # Particle position
        # Instantiate particle and add to list
        new_particle = Particle(PVector(x, y), canvas_size_x, canvas_size_y, all_particles, all_forces)
        all_particles.append(new_particle)
    
def draw():
    background(0)  # Clear canvas
    
    # Update and display all particles and forces
    for p in all_particles: p.run()
    for f in all_forces: f.run()

def mouseClicked():
    # Add new force on left click
    if mouseButton == LEFT:
        pos = PVector(mouseX, mouseY)  # Position of click
        force = PVector(random.uniform(-100, 100), random.uniform(-100, 100))  # Random force vector
        new_force = Force(pos, force)  # Create new force
        all_forces.append(new_force)  # Add to list
    
    # Add new particles on right click
    if mouseButton == RIGHT:
        for i in range(100):
            x, y = mouseX, mouseY  # Position of click
            # Instantiate particle and add to list
            new_particle = Particle(PVector(x, y), canvas_size_x, canvas_size_y, all_particles, all_forces)
            all_particles.append(new_particle)
