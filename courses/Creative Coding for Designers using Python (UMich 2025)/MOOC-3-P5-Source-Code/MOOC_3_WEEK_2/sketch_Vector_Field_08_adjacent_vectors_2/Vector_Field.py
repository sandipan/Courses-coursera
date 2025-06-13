from Force import Force
import random

class Vector_Field:
    # Initialize the vector field with dimensions and world size
    def __init__(self, cols, rows, world_x, world_y):
        self.cols = cols  # Number of columns in the grid
        self.rows = rows  # Number of rows in the grid
        self.all_forces = []  # List to store force vectors
        self.world_x = world_x  # Width of the world/canvas
        self.world_y = world_y  # Height of the world/canvas
        self.cell_size_x = float(self.world_x) / self.cols  # Calculate cell width
        self.cell_size_y = float(self.world_y) / self.rows  # Calculate cell height
        self.max_vec_size = 17  # Maximum vector size
        # Debugging: Print cell sizes to ensure they are calculated correctly
        println(self.cell_size_x)
        println(self.cell_size_y)
        self.phase_01 = 0.1  # Phase offset for noise in x direction
        self.phase_02 = 0.3  # Phase offset for noise in y direction
        self.initiate_vecfield()  # Populate the field with initial forces
     
           
    # Populate the vector field with initial force vectors
    def initiate_vecfield(self):
        for i in range(self.cols):
            for j in range(self.rows):
                # Position vector at cell center
                pos = PVector(i* self.cell_size_x + self.cell_size_x/2, 
                              j*self.cell_size_y + self.cell_size_y/2)
                # Generate noise-based vectors
                n = noise(i*0.1, j * 0.1)
                n2 = noise(i*0.04, j * 0.04)
                # Scale noise to vector size
                n = map(n, 0,1,-self.max_vec_size,self.max_vec_size)
                n2 = map(n2, 0,1,-self.max_vec_size,self.max_vec_size)
                # Create new force and add to list
                new_force = Force(pos, PVector(n,n2))
                self.all_forces.append(new_force)
                
    # Dynamically update vector field based on noise
    def animate_vecfield(self):
        # Increment phase offsets
        self.phase_01 += 0.01
        self.phase_02 += 0.03
        for i in range(self.cols):
            for j in range(self.rows):
                # Recalculate position for dynamic update
                pos = PVector(i* self.cell_size_x + self.cell_size_x/2, 
                              j*self.cell_size_y + self.cell_size_y/2)
                # Apply phase offsets to noise function
                n = noise(i*0.1 + self.phase_01, j * 0.1)
                n2 = noise(i*0.04, j * 0.04 + self.phase_02)
                # Scale and map noise to vector size
                n = map(n, 0,1,-self.max_vec_size,self.max_vec_size)
                n2 = map(n2, 0,1,-self.max_vec_size,self.max_vec_size)
                # Update force vectors
                new_force = Force(pos, PVector(n,n2))
                self.all_forces.append(new_force)
                
    # Execute actions to update and display the vector field
    def run(self):
        # self.all_forces = []  # Option to clear all forces before update (commented out)
        # self.animate_vecfield()  # Update vector field based on noise (commented out for static display)
        self.display()  # Display current state of the vector field

    # Display the vector field
    def display(self):
        # Run display function for each force vector
        for f in self.all_forces:
            f.run()

    # Generate relative moves for adjacent vector calculation
    def generate_moves(self, layers):
        moves = []
        for i in range(-layers, layers + 1):
            for j in range(-layers, layers + 1):
                if i != 0 or j != 0:  # Exclude the center
                    moves.append((i, j))
        return moves
   
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
            
    
    # Get indices of vectors adjacent to given coordinates with specified layers
    def get_adjacent_vectors(self, x, y, num_layers):
        adjacent_vectors = []
        moves = self.generate_moves(num_layers)  # Generate relative moves based on layers
        for dx, dy in moves:
            # Calculate adjusted position
            n_x = x + (dx * self.cell_size_x)
            n_y = y + (dy * self.cell_size_y)
            # Convert to grid coordinates
            n_x = int(n_x / (float(self.world_x) / self.cols))
            n_y = int(n_y / (float(self.world_y) / self.rows))
            # Calculate index if within bounds
            if 0 <= n_x < self.cols and 0 <= n_y < self.rows:
                index = (self.rows * n_x) + n_y
                adjacent_vectors.append(index)
        return adjacent_vectors
        
        
        
        
