from Force import Force
import random

class Vector_Field:
    # Initialize vector field with dimensions and world size
    def __init__(self, cols, rows, world_x, world_y):
        self.cols = cols  # Number of columns in vector field grid
        self.rows = rows  # Number of rows in vector field grid
        self.all_forces = []  # List to hold force vectors
        self.world_x = world_x  # Width of the simulation area
        self.world_y = world_y  # Height of the simulation area
        self.cell_size_x = float(world_x) / cols  # Width of each cell in the grid
        self.cell_size_y = float(world_y) / rows  # Height of each cell in the grid
        self.max_vec_size = 17  # Maximum size of force vectors
        self.phase_01 = 0.1  # Phase offset for noise in x direction
        self.phase_02 = 0.3  # Phase offset for noise in y direction
        self.initiate_vecfield()  # Populate the field with initial vectors
    
    # Populate the vector field with forces based on Perlin noise
    def initiate_vecfield(self):
        for i in range(self.cols):
            for j in range(self.rows):
                pos = PVector(i * self.cell_size_x + self.cell_size_x / 2, 
                              j * self.cell_size_y + self.cell_size_y / 2)
                n = noise(i * 0.1, j * 0.1)  # Generate noise value for x component
                n2 = noise(i * 0.04, j * 0.04)  # Generate noise value for y component
                # Map noise to force vector size
                n = map(n, 0, 1, -self.max_vec_size, self.max_vec_size)
                n2 = map(n2, 0, 1, -self.max_vec_size, self.max_vec_size)
                # Create and add new force based on noise
                new_force = Force(pos, PVector(n, n2))
                self.all_forces.append(new_force)
                
    # Dynamically update vector field based on changing noise values
    def animate_vecfield(self):
        self.phase_01 += 0.01  # Increment phase for x noise
        self.phase_02 += 0.03  # Increment phase for y noise
        # Recreate forces with updated noise values
        for i in range(self.cols):
            for j in range(self.rows):
                pos = PVector(i * self.cell_size_x + self.cell_size_x / 2, 
                              j * self.cell_size_y + self.cell_size_y / 2)
                n = noise(i * 0.1 + self.phase_01, j * 0.1)
                n2 = noise(i * 0.04, j * 0.04 + self.phase_02)
                n = map(n, 0, 1, -self.max_vec_size, self.max_vec_size)
                n2 = map(n2, 0, 1, -self.max_vec_size, self.max_vec_size)
                new_force = Force(pos, PVector(n, n2))
                self.all_forces.append(new_force)
                
    # Execute actions to update and display the vector field
    def run(self):
        # self.all_forces = []  # Option to clear all forces before update (commented out)
        # self.animate_vecfield()  # Update vector field based on noise (commented out for static display)
        self.display()  # Display current state of the vector field
        
        
    # Display all forces in the vector field
    def display(self):
        for f in self.all_forces:
            f.run()  # Display each force
            
    # Generate relative moves for calculating adjacent vectors
    def generate_moves(self, layers):
        moves = []  # List to hold move patterns
        # Generate move patterns excluding the center point
        for i in range(-layers, layers + 1):
            for j in range(-layers, layers + 1):
                if i != 0 or j != 0:
                    moves.append((i, j))
        return moves
    
    # Get indices of adjacent vectors based on position and layer depth
    def get_adjacent_vectors(self, x, y, num_layers):
        adjacent_vectors = []  # List to hold indices of adjacent vectors
        moves = self.generate_moves(num_layers)  # Get move patterns
        # Calculate positions of adjacent vectors
        for dx, dy in moves:
            n_x = x + (dx * self.cell_size_x)
            n_y = y + (dy * self.cell_size_y)
            n_x = int(n_x / (self.world_x / self.cols))
            n_y = int(n_y / (self.world_y / self.rows))
            index = (self.rows * n_x) + n_y  # Calculate index in list
            if 0 <= n_x < self.cols and 0 <= n_y < self.rows:
                adjacent_vectors.append(index)
        return adjacent_vectors
    
    # Get the index of the force at specific coordinates
    def get_force(self, x, y):
        # Convert to grid coordinates
        x = int(x / (float(self.world_x) / self.cols))
        y = int(y / (float(self.world_y) / self.rows))
        # Calculate index
        index = (self.rows * x) + y
        # Return index if within bounds
        if 0 <= index < len(self.all_forces):
            return index
        else:
            raise IndexError("Vector index out of range.")
    
    # Set force vector at specific index
    def set_force(self, index, new_force):
        if index < len(self.all_forces):
            self.all_forces[index].v_force = new_force

    # Add to the force vector at specific index
    def add_force(self, index, new_force):
        if index < len(self.all_forces):
            self.all_forces[index].v_force.add(new_force)
        
        
        
        
