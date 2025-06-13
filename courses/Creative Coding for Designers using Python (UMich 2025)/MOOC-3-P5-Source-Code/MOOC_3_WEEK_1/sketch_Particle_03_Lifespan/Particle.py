import random

class Particle:
    # Initialize particle with position, canvas dimensions, and reference to particle list
    def __init__(self, pos, world_x, world_y, part_list):
        self.pos = pos  # Particle position
        self.world_x = world_x  # Canvas width
        self.world_y = world_y  # Canvas height
        self.lifespan = random.randrange(100,200)  # Random lifespan
        x_vel = random.uniform(-1,1)  # Horizontal velocity
        y_vel = random.uniform(-1,1)  # Vertical velocity
        self.vel = PVector(x_vel,y_vel)  # Velocity vector
        self.acc = PVector(0,0)  # Acceleration vector
        self.gravity = PVector(0,0.01)  # Gravity effect
        self.part_list = part_list  # Reference to the list holding this particle
        self.count = 0  # Initialize count for lifespan tracking
    
    # Core loop: display, apply forces, update state, check for death
    def run(self):
        self.display()
        self.compute_forces()
        self.update()
        self.die()
        
    # Update velocity and position; reset acceleration
    def update(self):
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc = PVector(0,0)
        
    # Apply gravity to acceleration
    def compute_forces(self):
        self.acc.add(self.gravity)
        
    # Remove particle from list when it dies
    def die(self):
        self.count += 1
        if self.count >= self.lifespan:
            self.part_list.remove(self)
        
    # Display particle as ellipse
    def display(self):
        stroke(255)  # Outline color
        fill(0,0,255)  # Fill color
        ellipse(self.pos.x, self.pos.y, 5, 5)  # Draw particle
