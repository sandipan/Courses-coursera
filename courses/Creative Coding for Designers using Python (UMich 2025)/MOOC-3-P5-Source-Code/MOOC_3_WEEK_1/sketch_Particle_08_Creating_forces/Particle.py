import random

class Particle:
    # Initializes particle with attributes and lists it interacts with
    def __init__(self, pos, world_x, world_y, part_list, force_list):
        self.pos = pos  # Position vector
        self.world_x = world_x  # Canvas width
        self.world_y = world_y  # Canvas height
        self.lifespan = 300  # Lifespan of the particle
        # Initial velocity with random components
        x_vel = random.uniform(-1,1)
        y_vel = random.uniform(-1,1)
        z_vel = random.uniform(-1,1)
        self.vel = PVector(x_vel,y_vel,z_vel)  # Velocity vector
        self.acc = PVector(0,0,0)  # Acceleration vector
        self.count = 0  # Age counter
        self.gravity = PVector(0,0.01)  # Gravity effect
        self.part_list = part_list  # List of all particles
        self.trail = []  # Trail history for visual effect
        self.force_list = force_list  # List of forces affecting the particle
        self.closest_force_id = -1  # Index of the closest force

    # Main method to run particle behaviors
    def run(self):
        self.display()  # Visual representation of particle
        self.update_trail()  # Updates trail for drawing
        self.closest_force()  # Determines closest force effect
        self.compute_forces()  # Applies forces to particle
        self.update()  # Updates particle's position
        self.die()  # Checks if particle should be removed based on lifespan
        
    # Identifies the closest force effect to the particle
    def closest_force(self):
        closest_dist = 1000000  # Large initial value for comparison
        closest_id = -1  # Placeholder for the closest force index
        for i in range(len(self.force_list)):
            dif = self.pos.copy().sub(self.force_list[i].pos)  # Difference vector to force
            dist_to_force = dif.mag()  # Distance to the force
            if(dist_to_force < closest_dist):  # Update if closer force is found
                closest_dist = dist_to_force
                closest_id = i
        self.closest_force_id = closest_id  # Store closest force index
        # Visual line to closest force
        stroke(255,50)
        line(self.pos.x, self.pos.y, self.force_list[closest_id].pos.x, self.force_list[closest_id].pos.y)
        
    # Updates the trail for visual effect
    def update_trail(self):
        if(frameCount % 8 == 0):  # Every 8 frames
            self.trail.append(self.pos.copy())  # Add current position to trail
            if len(self.trail) > 15:  # Limit trail length
                self.trail.pop(0)
        
    # Updates particle's motion
    def update(self):
        self.vel.add(self.acc)  # Apply acceleration to velocity
        self.pos.add(self.vel)  # Apply velocity to position
        self.acc = PVector(0,0,0)  # Reset acceleration for next cycle
        
    # Applies forces to the particle
    def compute_forces(self):
        # Not adding gravity directly to keep the focus on other forces
        if self.closest_force_id != -1:  # Ensure there's a closest force
            clo_force_pos = self.force_list[self.closest_force_id].pos  # Position of closest force
            vec = self.force_list[self.closest_force_id].v_force.copy()  # Copy of the force vector
            dif = self.pos.copy().sub(clo_force_pos)  # Vector difference to force
            dist_to_force_sqr = dif.mag()**2  # Square of distance to force for inverse square law
            force_factor = vec.mag() / dist_to_force_sqr  # Calculate force factor
            vec.normalize()  # Normalize force direction
            vec.mult(force_factor * 3)  # Apply force factor
            self.acc.add(vec)  # Update acceleration with force vector
        
    # Checks and processes particle's death
    def die(self):
        self.count += 1  # Increment age
        if(self.count >= self.lifespan):  # Check lifespan
            self.part_list.remove(self)  # Remove from particle list
        
    # Draws particle and its trail
    def display(self):
        stroke(255)  # White for particle outline
        fill(0,0,255)  # Blue for particle fill
        ellipse(self.pos.x, self.pos.y, 5, 5)  # Draw particle
        # Draw each segment of the trail
        for i in range(1, len(self.trail)):
            stroke(255,0,0)  # Red for
