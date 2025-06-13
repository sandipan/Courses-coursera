import random

class Particle:
    # Initializes a new instance of the Particle class
    def __init__(self, pos, world_x, world_y):
        self.pos = pos  # Current position of the particle
        self.world_x = world_x  # Width of the environment or canvas
        self.world_y = world_y  # Height of the environment or canvas
        # Set the particle's velocity to a random vector
        x_vel = random.uniform(-1, 1)
        y_vel = random.uniform(-1, 1)
        z_vel = random.uniform(-1, 1)
        self.vel = PVector(x_vel, y_vel, z_vel)
        self.acc = PVector(0, 0, 0)  # Initialize acceleration to zero
        self.gravity = PVector(0, 0.01)  # A constant force simulating gravity

    # Method to be called every frame to update and draw the particle
    def run(self):
        self.display()  # Draw the particle
        self.compute_forces()  # Apply forces to the particle
        self.update()  # Update the particle's position and velocity
    
    # Updates the particle's position and velocity
    def update(self):
        self.vel.add(self.acc)  # Add acceleration to velocity
        self.pos.add(self.vel)  # Add velocity to position
        self.acc = PVector(0, 0, 0)  # Reset acceleration after each update
        
    # Computes the forces affecting the particle
    def compute_forces(self):
        self.acc.add(self.gravity)  # Apply gravity to acceleration
        
    # Draws the particle on the canvas
    def display(self):
        stroke(255)  # Set the stroke color to white
        fill(0, 0, 255)  # Set the fill color to blue
        ellipse(self.pos.x, self.pos.y, 5, 5)  # Draw an ellipse at the particle's position
