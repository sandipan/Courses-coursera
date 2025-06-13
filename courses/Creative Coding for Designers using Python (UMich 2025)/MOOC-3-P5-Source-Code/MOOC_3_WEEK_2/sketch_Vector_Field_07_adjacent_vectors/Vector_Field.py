from Force import Force
import random

class Vector_Field:
    # Initialize vector field with grid dimensions and world dimensions
    def __init__(self, cols, rows, world_x, world_y):
        self.cols = cols  # Columns in the field
        self.rows = rows  # Rows in the field
        self.all_forces = []  # Store force vectors
        self.world_x = world_x  # Canvas width
        self.world_y = world_y  # Canvas height
        # Calculate size of each cell in x and y dimensions
        self.cell_size_x = float(self.world_x) / self.cols
        self.cell_size_y = float(self.world_y) / self.rows
        self.max_vec_size = 17  # Max vector magnitude
        # Debugging: print cell sizes to ensure correct calculation
        println(self.cell_size_x)
        println(self.cell_size_y)
        self.phase_01 = 0.1  # Initial phase for noise function
        self.phase_02 = 0.3  # Secondary phase for noise function
        self.initiate_vecfield()  # Populate the field with initial forces

    # Populate vector field with forces
    def initiate_vecfield(self):
        for i in range(self.cols):
            for j in range(self.rows):
                # Calculate force position at cell center
                pos = PVector(i* self.cell_size_x + self.cell_size_x/2, 
                              j*self.cell_size_y + self.cell_size_y/2)
                # Use noise for natural variation in force direction
                n = noise(i*0.1, j * 0.1)
                n2 = noise(i*0.04, j * 0.04)
                # Scale noise values to vector sizes
                n = map(n, 0,1,-self.max_vec_size,self.max_vec_size)
                n2 = map(n2, 0,1,-self.max_vec_size,self.max_vec_size)
                # Create and add new force
                new_force = Force(pos, PVector(n,n2))
                self.all_forces.append(new_force)
                
    # Animate the vector field by updating forces
    def animate_vecfield(self):
        self.phase_01 += 0.01  # Increment phase for varied animation
        self.phase_02 += 0.03
        
        for i in range(self.cols):
            for j in range(self.rows):
                # Recalculate position at cell center
                pos = PVector(i* self.cell_size_x + self.cell_size_x/2, 
                              j*self.cell_size_y + self.cell_size_y/2)
                # Update noise with phases for animation
                n = noise(i*0.1 + self.phase_01, j * 0.1)
                n2 = noise(i*0.04, j * 0.04 + self.phase_02)
                n = map(n, 0,1,-self.max_vec_size,self.max_vec_size)
                n2 = map(n2, 0,1,-self.max_vec_size,self.max_vec_size)
                # Recreate forces with updated directions
                new_force = Force(pos, PVector(n,n2))
                self.all_forces.append(new_force)
                
    def run(self):
        # Refresh and display vector field
        # self.all_forces = []  # Uncomment to clear forces before animation
        # self.animate_vecfield()  # Uncomment to animate vector field
        self.display()  # Display current state of vector field
        
    def display(self):
        # Display all forces in the field
        for f in self.all_forces:
            f.run()
            
    def get_force(self, x, y):
        # Convert screen position to grid coordinates
        x = int(x / (float(self.world_x) / self.cols))
        y = int(y / (float(self.world_y) / self.rows))
        
        # Calculate index in the list based on grid coordinates
        index = (self.rows * x) + y
        
        # Debugging: print calculated index and grid coordinates
        print("index: " + str(index) + " , x: " + str(x) + ", y: " + str(y))
        
        # Return corresponding force if index is valid
        if 0 <= index < len(self.all_forces):
            return self.all_forces[index]
        else:
            raise IndexError("Vector index out of range.")  # Handle out-of-range access
    
    # Replace the force vector at the specified index with a new force
    def set_force(self, index, new_force):
        if index < len(self.all_forces):  # Ensure index is within bounds
            self.all_forces[index].v_force = new_force  # Set new force vector
    
    # Add a force vector to the existing force vector at the specified index
    def add_force(self, index, new_force):
        if index < len(self.all_forces):  # Ensure index is within bounds
            self.all_forces[index].v_force.add(new_force)  # Add new force to existing force vector


    # Retrieve indices of vectors adjacent to a given position
    def get_adjacent_vectors(self, x, y):
        adjacent_vectors = []  # Initialize list to store indices of adjacent vectors
        
        # Define relative moves to find adjacent positions in grid
        moves = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),          (0, 1),
                 (1, -1),  (1, 0), (1, 1)]
        
        # Iterate through defined moves to check adjacent positions
        for dx, dy in moves:
            # Calculate new position based on move
            n_x = x + (dx * self.cell_size_x)
            n_y = y + (dy * self.cell_size_y)
            
            # Convert new position to grid coordinates
            n_x = int(n_x / (float(self.world_x) / self.cols))
            n_y = int(n_y / (float(self.world_y) / self.rows))
            
            # Calculate index in the flat list of forces
            index = (self.rows * n_x) + n_y
            
            # If calculated position is within bounds, add its index to the list
            if 0 <= n_x < self.cols and 0 <= n_y < self.rows:
                adjacent_vectors.append(index)
        
        # Return list of indices for adjacent vectors
        return adjacent_vectors

        
        
        
        
