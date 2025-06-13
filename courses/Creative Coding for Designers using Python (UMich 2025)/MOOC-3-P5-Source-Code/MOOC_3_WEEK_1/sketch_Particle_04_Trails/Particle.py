import random

class Particle:
    # Initialize particle with position, canvas dimensions, lifespan, velocity, acceleration, and trail
    def __init__(self, pos, world_x, world_y, part_list):
        self.pos = pos  # Position vector
        self.world_x = world_x  # Canvas width
        self.world_y = world_y  # Canvas height
        self.lifespan = 1000  # Lifespan of the particle
        # Velocity components with random direction
        x_vel = random.uniform(-1,1)
        y_vel = random.uniform(-1,1)
        self.vel = PVector(x_vel,y_vel)  # Velocity vector
        self.acc = PVector(0,0)  # Acceleration vector, initialized to zero
        self.count = 0  # Frame count for tracking lifespan
        self.gravity = PVector(0,0.01)  # Gravity force
        self.part_list = part_list  # Reference to the list holding this particle
        self.trail = []  # List to store positions for drawing trails
    
    # Runs particle behavior each frame
    def run(self):
        self.display()  # Draw particle
        self.update_trail()  # Update its trail
        #self.compute_forces()  # Apply forces (commented out)
        self.update()  # Update position and velocity
        self.die()  # Check lifespan and remove if necessary
    
    # Update the trail of the particle
    def update_trail(self):
        if frameCount % 8 == 0:  # Add to trail every 8 frames
            self.trail.append(self.pos.copy())  # Copy current position
            if len(self.trail) > 15:  # Keep trail length to max 15
                self.trail.pop(0)  # Remove oldest position
            
    # Update particle's velocity and position
    def update(self):
        self.vel.add(self.acc)  # Apply acceleration to velocity
        self.pos.add(self.vel)  # Apply velocity to position
        self.acc = PVector(0,0)  # Reset acceleration
        
    # Add gravity to acceleration
    def compute_forces(self):
        self.acc.add(self.gravity)
        
    # Remove particle from list if lifespan is exceeded
    def die(self):
        self.count += 1
        if self.count >= self.lifespan:
            self.part_list.remove(self)
        
    # Display particle and its trail
    def display(self):
        stroke(255)  # White stroke for particle
        fill(0,0,255)  # Blue fill for particle
        ellipse(self.pos.x, self.pos.y, 5, 5)  # Draw particle
        
        # Draw trail
        for i in range(1, len(self.trail)):
            noStroke()
            fill(255,0,0)  # Red fill for trail
            # Draw line for each segment in the trail
            stroke(255,0,0)  # Red stroke for trail lines
            line(self.trail[i].x, self.trail[i].y, 
                 self.trail[i-1].x, self.trail[i-1].y)
