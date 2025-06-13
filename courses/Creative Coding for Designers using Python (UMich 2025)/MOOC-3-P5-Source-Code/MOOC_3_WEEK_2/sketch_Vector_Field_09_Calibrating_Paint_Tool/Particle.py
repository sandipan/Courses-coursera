import random

class Particle:
    # Initialize particle with position, canvas dimensions, and relevant lists
    def __init__(self, pos, world_x, world_y, part_list, force_list):
        self.pos = pos  # Particle position
        self.world_x = world_x  # Canvas width
        self.world_y = world_y  # Canvas height
        self.lifespan = 1000  # Particle lifespan
        # Random velocity components
        x_vel = random.uniform(-1, 1)
        y_vel = random.uniform(-1, 1)
        z_vel = random.uniform(-1, 1)
        self.vel = PVector(x_vel, y_vel, z_vel)  # Velocity vector
        self.acc = PVector(0, 0, 0)  # Acceleration vector
        self.count = 0  # Age counter
        self.gravity = PVector(0, 0.01)  # Gravity vector
        self.part_list = part_list  # Particle list reference
        self.trail = []  # Trail history for visual effect
        self.force_list = force_list  # Force list reference
        self.closest_force_id = -1  # ID of closest force
    
    def run(self):
        self.display()  # Display particle
        self.update_trail()  # Update trail effect
        self.closest_force()  # Determine closest force
        self.compute_forces()  # Compute force effects
        self.update()  # Update particle state
        self.die()  # Check for particle death
        
        
    def closest_force(self):
        closest_dist = 1000000  # Start with a large number for comparison
        closest_id = -1  # Initialize with invalid index
        for i in range(len(self.force_list)):  # Iterate through all forces
            dif = self.pos.copy().sub(self.force_list[i].pos)  # Calculate vector difference between particle and force position
            dist_to_force = dif.mag()  # Calculate magnitude of difference vector as distance
            if(dist_to_force < closest_dist):  # If current distance is smaller than what we have found so far
                closest_dist = dist_to_force  # Update closest distance
                closest_id = i  # Update closest force's index
                    
        closest_force = self.force_list[closest_id]  # Retrieve closest force 
        self.closest_force_id = closest_id  # Update particle's closest force id
        stroke(255,50)  # Set line color for drawing
        line(self.pos.x, self.pos.y, closest_force.pos.x, closest_force.pos.y)  # Draw a line from particle to closest force 

    
    def update_trail(self):
        # Update particle's trail every 8 frames
        if(frameCount % 8 == 0):
            self.trail.append(self.pos.copy())  # Add current position to trail
            if len(self.trail) > 15:  # Limit trail length
                self.trail.pop(0)
            
        
    def update(self):
        self.vel.add(self.acc)  # Apply acceleration to velocity
        self.pos.add(self.vel)  # Update position with velocity
        self.acc = PVector(0, 0, 0)  # Reset acceleration
        
    def compute_forces(self):
        # Compute force based on closest force's influence
        vec = self.force_list[self.closest_force_id].v_force.copy()  # Force vector
        dif = self.pos.copy().sub(self.force_list[self.closest_force_id].pos)  # Position difference
        dist_to_force = dif.mag()  # Distance to force
        force_factor = map(dist_to_force, 0, 2000, 0.0002, 0)  # Scale force based on distance
        vec.mult(force_factor)  # Apply force factor
        self.acc.add(vec)  # Update acceleration with force
        
    def die(self):
        self.count += 1  # Increment age
        if(self.count >= self.lifespan):  # Check if lifespan is exceeded
            self.part_list.remove(self)  # Remove particle from list

    def display(self):
        # Display particle and its trail
        stroke(255)  # White stroke for particle
        fill(0, 0, 255)  # Blue fill for particle
        ellipse(self.pos.x, self.pos.y, 5, 5)  # Draw particle
        # Draw particle's trail
        for i in range(1, len(self.trail)):
            stroke(255, 0, 0)  # Red stroke for trail
            line(self.trail[i-1].x, self.trail[i-1].y, self.trail[i].x, self.trail[i].y)  # Draw trail line
            
            
            
            
