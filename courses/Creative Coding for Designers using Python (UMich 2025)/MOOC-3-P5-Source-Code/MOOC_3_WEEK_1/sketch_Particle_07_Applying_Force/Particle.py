import random

class Particle:
    # Initializes a new Particle instance
    def __init__(self, pos, world_x, world_y, part_list, force_list):
        self.pos = pos  # Particle's position
        self.world_x = world_x  # Canvas width
        self.world_y = world_y  # Canvas height
        self.lifespan = 2000  # Lifespan of the particle
        # Random initial velocity
        x_vel = random.uniform(-1,1)
        y_vel = random.uniform(-1,1)
        self.vel = PVector(x_vel, y_vel)  # Velocity vector
        self.acc = PVector(0, 0)  # Acceleration vector
        self.count = 0  # Age counter
        self.gravity = PVector(0, 0.01)  # Gravity effect
        self.part_list = part_list  # Reference to the list of particles
        self.trail = []  # Trail positions for visual effect
        self.force_list = force_list  # Forces affecting the particle
        self.closest_force_id = -1  # Index of the closest force

    # Runs particle behavior per frame
    def run(self):
        self.display()  # Show particle
        self.update_trail()  # Update its trail
        self.closest_force()  # Find and react to the closest force
        self.compute_forces()  # Apply forces
        self.update()  # Update state
        self.die()  # Check for lifespan expiration

    # Identifies the closest force to the particle
    def closest_force(self):
        closest_dist = float('inf')  # Initialize closest distance as infinity for comparison
        closest_id = -1  # Initialize ID of the closest force as -1 (not found state)
        for i, force in enumerate(self.force_list):  # Iterate over all forces
            dif = self.pos.copy().sub(force.pos)  # Calculate vector difference between particle and force positions
            dist_to_force = dif.mag()  # Calculate magnitude of the vector for distance
            if dist_to_force < closest_dist:  # If found distance is shorter, update closest force info
                closest_dist = dist_to_force
                closest_id = i
        self.closest_force_id = closest_id  # Update the particle's closest force ID with the found closest force


    # Update the particle's trail for visual effect
    def update_trail(self):
        if frameCount % 8 == 0:
            self.trail.append(self.pos.copy())  # Add current position to the trail
            if len(self.trail) > 15:  # Limit trail length
                self.trail.pop(0)

    # Update particle's position and velocity
    def update(self):
        self.vel.add(self.acc)  # Apply acceleration
        self.pos.add(self.vel)  # Move particle
        self.acc = PVector(0, 0)  # Reset acceleration

    # Calculates and applies forces to the particle
    def compute_forces(self):
        if self.closest_force_id >= 0:  # Ensure there is a closest force
            # Compute force vector based on the closest force's characteristics
            force = self.force_list[self.closest_force_id]
            force_vec = force.calculate_force(self.pos)
            self.acc.add(force_vec)  # Apply force vector to acceleration

    # Removes the particle if its lifespan is exceeded
    def die(self):
        self.count += 1  # Increment age
        if self.count >= self.lifespan:  # Check if lifespan is reached
            self.part_list.remove(self)  # Remove particle from the list

    # Draws the particle and its trail
    def display(self):
        # Particle itself
        stroke(255)  # White outline
        fill(0, 0, 255)  # Blue fill
        ellipse(self.pos.x, self.pos.y, 5, 5)  # Draw particle
        # Particle's trail
        for i in range(1, len(self.trail)):
            stroke(255, 0, 0)  # Red line for trail
            line(self.trail[i-1].x, self.trail[i-1].y, self.trail[i].x, self.trail[i].y)  # Draw trail segment
