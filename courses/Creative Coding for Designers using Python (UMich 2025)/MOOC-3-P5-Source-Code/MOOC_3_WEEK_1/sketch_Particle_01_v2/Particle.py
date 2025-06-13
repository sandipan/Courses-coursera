import random

class Particle:
    # Particle class constructor
    def __init__(self, pos, world_x, world_y):
        # Initialize position, world dimensions, velocity, acceleration, and counter
        self.pos = pos             # Current position of the particle
        self.world_x = world_x     # Width of the world (or canvas)
        self.world_y = world_y     # Height of the world (or canvas)
        x_vel = random.uniform(-1, 1)  # Random X velocity between -1 and 1
        y_vel = random.uniform(-1, 1)  # Random Y velocity between -1 and 1
        z_vel = random.uniform(-1, 1)  # Random Z velocity between -1 and 1 (for 3D)
        self.vel = PVector(x_vel, y_vel, z_vel)  # Velocity vector
        self.acc = PVector(0, 0, 0)  # Acceleration vector (initialized to 0)

    # Method to update and display the particle each frame
    def run(self):
        self.display()  # Render particle
        self.update()   # Update particle's properties

    # Update particle's position based on its velocity
    def update(self):
        self.pos.add(self.vel)  # Add velocity to position

    # Render the particle on the canvas
    def display(self):
        stroke(255)  # Set stroke color to white
        fill(0, 0, 255)  # Set fill color to blue
        ellipse(self.pos.x, self.pos.y, 5, 5)  # Draw the particle as a small ellipse
