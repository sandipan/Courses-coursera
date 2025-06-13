import random

class Particle:
    # Initialize with position, canvas bounds, and list reference
    def __init__(self, pos, world_x, world_y, part_list):
        self.pos = pos  # Position vector
        self.world_x = world_x  # Canvas width
        self.world_y = world_y  # Canvas height
        self.lifespan = 1000  # Lifespan of the particle
        # Random initial velocity
        x_vel = random.uniform(-1,1)
        y_vel = random.uniform(-1,1)
        self.vel = PVector(x_vel,y_vel)  # Velocity vector
        self.acc = PVector(0,0)  # Acceleration vector
        self.count = 0  # Age counter
        self.gravity = PVector(0,0.01)  # Gravity vector
        self.part_list = part_list  # Reference to the particle list
        self.trail = []  # List for storing trail positions
    
    # Main method to handle particle logic
    def run(self):
        self.display()  # Show particle
        self.update_trail()  # Update its trail
        self.update()  # Update physics
        self.die()  # Check for particle's death
    
    # Update particle trail
    def update_trail(self):
        if frameCount % 8 == 0:  # Every 8 frames
            self.trail.append(self.pos.copy())  # Add position copy to trail
            if len(self.trail) > 15:  # Keep trail length to 15
                self.trail.pop(0)  # Remove oldest position
            
    # Update particle's physics
    def update(self):
        self.vel.add(self.acc)  # Apply acceleration to velocity
        self.pos.add(self.vel)  # Apply velocity to position
        self.acc = PVector(0,0,0)  # Reset acceleration
        
    # Method for gravity effect (unused here)
    def compute_forces(self):
        self.acc.add(self.gravity)  # Apply gravity to acceleration
        
    # Check and handle particle's death
    def die(self):
        self.count += 1
        if self.count >= self.lifespan:  # If lifespan exceeded
            self.part_list.remove(self)  # Remove from particle list
        
    # Display particle and its trail
    def display(self):
        stroke(255)  # White stroke color
        fill(0,0,255)  # Blue fill color
        ellipse(self.pos.x, self.pos.y, 5, 5)  # Draw particle as ellipse
        
        # Draw trail
        for i in range(1, len(self.trail)):
            stroke(255,0,0)  # Red stroke color for trail
            line(self.trail[i].x, self.trail[i].y, 
                 self.trail[i-1].x, self.trail[i-1].y)  # Line between trail segments
