import random

class Particle:
    # Initialize particle with position, world dimensions, particle and force lists
    def __init__(self, pos, world_x, world_y, part_list, force_list):
        self.pos = pos  # Current position
        self.world_x = world_x  # Canvas width
        self.world_y = world_y  # Canvas height
        self.lifespan = 1000  # Lifespan of the particle
        # Random velocity components
        x_vel = random.uniform(-1,1)
        y_vel = random.uniform(-1,1)
        self.vel = PVector(x_vel,y_vel)  # Velocity vector
        self.acc = PVector(0,0,0)  # Acceleration vector
        self.count = 0  # Age counter
        self.gravity = PVector(0,0.01)  # Gravity force
        self.part_list = part_list  # Reference to the particle list
        self.trail = []  # List to hold trail positions
        self.force_list = force_list  # Reference to the force list
        self.closest_force_id = -1  # ID of the closest force
    
    # Main loop to handle particle behavior
    def run(self):
        self.display()  # Display particle
        self.update_trail()  # Update its trail
        self.closest_force()  # Determine and draw line to closest force
        self.update()  # Update physics
        self.die()  # Check lifespan and remove if necessary
        
    # Determine closest force and draw a line to it
    def closest_force(self):
        closest_dist = 1000000  # Initial large distance
        closest_id = -1  # Placeholder for closest force ID
        # Loop through all forces to find the closest
        for i in range(len(self.force_list)):
            dif = self.pos.copy().sub(self.force_list[i].pos)  # Calculate difference vector
            dist_to_force = dif.mag()  # Distance to this force
            if(dist_to_force < closest_dist):  # Update closest force if closer
                closest_dist = dist_to_force
                closest_id = i
        closest_force = self.force_list[closest_id]  # Closest force object
        self.closest_force_id = closest_id  # Store closest force ID
        stroke(255,50)  # Set stroke for line
        # Draw line to closest force
        line(self.pos.x, self.pos.y, closest_force.pos.x, closest_force.pos.y)
    
    # Update trail positions
    def update_trail(self):
        if(frameCount % 8 == 0):  # Every 8 frames
            self.trail.append(self.pos.copy())  # Add current position to trail
            if (len(self.trail) > 15):  # Keep trail to last 15 positions
                self.trail.pop(0)  # Remove oldest position
        
    # Update particle's position and velocity
    def update(self):
        self.vel.add(self.acc)  # Apply acceleration to velocity
        self.pos.add(self.vel)  # Apply velocity to position
        self.acc = PVector(0,0)  # Reset acceleration after each frame
        
    # Add gravity force to acceleration (method placeholder, not called)
    def compute_forces(self):
        self.acc.add(self.gravity)  # Apply gravity
        
    # Check if particle should be removed based on its lifespan
    def die(self):
        self.count += 1  # Increment age counter
        if(self.count >= self.lifespan):  # If lifespan exceeded
            self.part_list.remove(self)  # Remove from particle list
        
    # Display particle and its trail
    def display(self):
        stroke(255)  # White stroke for particle
        fill(0,0,255)  # Blue fill for particle
        ellipse(self.pos.x, self.pos.y, 5, 5)  # Draw particle
        
        # Draw trail
        for i in range(1, len(self.trail)):
            stroke(255,0,0)  # Red stroke for trail
            # Draw line segment for trail
            line(self.trail[i].x, self.trail[i].y, 
                 self.trail[i-1].x, self.trail[i-1].y)
