from Force import Force
import random

class Vector_Field:
    # Constructor for the Vector_Field class
    def __init__(self, cols, rows, world_x, world_y):
        self.cols = cols                # Number of columns in the vector field
        self.rows = rows                # Number of rows in the vector field
        self.all_forces = []            # List to store all force vectors
        self.world_x = world_x          # Width of the vector field area
        self.world_y = world_y          # Height of the vector field area
        # Calculate the size of each cell in the grid
        self.cell_size_x = float(world_x) / cols
        self.cell_size_y = float(world_y) / rows
        self.max_vec_size = 17          # Maximum size of the vector
        # Print cell sizes for verification
        println(self.cell_size_x)
        println(self.cell_size_y)
        # Phases for animating the vector field
        self.phase_01 = 0.1
        self.phase_02 = 0.3
        self.initiate_vecfield()  # Populate the field with initial forces

    # Initialize the vector field with forces
    def initiate_vecfield(self):
        for i in range(self.cols):
            for j in range(self.rows):
                # Calculate the position of each force in the grid
                pos = PVector(i * self.cell_size_x + self.cell_size_x / 2, 
                              j * self.cell_size_y + self.cell_size_y / 2)
                
                # Generate noise values and map them to vector sizes
                n = noise(i * 0.1, j * 0.1)
                n2 = noise(i * 0.04, j * 0.04)
                n = map(n, 0, 1, -self.max_vec_size, self.max_vec_size)
                n2 = map(n2, 0, 1, -self.max_vec_size, self.max_vec_size)
              
                # Create a new force and add it to the list
                new_force = Force(pos, PVector(n, n2))
                self.all_forces.append(new_force)

    # Animate the vector field by updating forces
    def animate_vecfield(self):
        # Update the phases for noise calculation
        self.phase_01 += 0.01
        self.phase_02 += 0.03
        
        for i in range(self.cols):
            for j in range(self.rows):
                # Calculate the position for each force
                pos = PVector(i * self.cell_size_x + self.cell_size_x / 2, 
                              j * self.cell_size_y + self.cell_size_y / 2)
                
                # Generate new noise values with phases and map them
                n = noise(i * 0.1 + self.phase_01, j * 0.1)
                n2 = noise(i * 0.04, j * 0.04 + self.phase_02)
                n = map(n, 0, 1, -self.max_vec_size, self.max_vec_size)
                n2 = map(n2, 0, 1, -self.max_vec_size, self.max_vec_size)
            
                # Create a new force and add it to the list
                new_force = Force(pos, PVector(n, n2))
                self.all_forces.append(new_force)
                
    def get_force(self, x, y):
        # Convert the x-coordinate to the corresponding column in the vector field
        x = int(x / (float(self.world_x) / self.cols))
        # Convert the y-coordinate to the corresponding row in the vector field
        y = int(y / (float(self.world_y) / self.rows))
        
        # Calculate the index in the flat list (1D array) based on the 2D grid coordinates
        index = y * self.cols + x
        
        # Debugging print statement: prints the calculated index and the grid coordinates
        print("index: " + str(index) + " , x: " + str(x) + ", y: " + str(y)) 
        
        # Check if the index is within the range of the all_forces list
        if 0 <= index < len(self.all_forces):
            # Return the force vector at the calculated index
            return self.all_forces[index]
        else:
            # If the index is out of range, raise an IndexError
            raise IndexError("Vector index out of range.")
            
    # Replace the force vector at the specified index with a new force
    def set_force(self, index, new_force):
        if index < len(self.all_forces):  # Ensure index is within bounds
            self.all_forces[index].v_force = new_force  # Set new force vector
    
    # Add a force vector to the existing force vector at the specified index
    def add_force(self, index, new_force):
        if index < len(self.all_forces):  # Ensure index is within bounds
            self.all_forces[index].v_force.add(new_force)  # Add new force to existing force vector
            
    def get_adjacent_vectors(self, x, y):
        # List to store the indices of adjacent vectors
        adjacent_vectors = []
        
        # Define relative moves to get adjacent positions
        # Each tuple represents a direction (dx, dy)
        '''
        moves = [ (-1, -1), (-1, 0), (-1, 1),
                ( 0, -1),          ( 0, 1),
                ( 1, -1),  (1, 0), ( 1, 1)
                ]
        '''
        moves = self.generate_moves(num_layers)
        
        # Iterate through each possible adjacent direction
        for dx, dy in moves:
            # Calculate the new x and y positions by adding the relative moves
            n_x = x + (dx * self.cell_size_x)
            n_y = y + (dy * self.cell_size_y)
            
            # Convert these positions to column and row indices in the vector field grid
            n_x = int(n_x / (float(self.world_x) / self.cols))
            n_y = int(n_y / (float(self.world_y) / self.rows))
            
            # Calculate the flat list index of the adjacent vector
            index = n_y * self.cols + n_x
            
            # Check if the calculated position is within the bounds of the vector field
            if 0 <= n_x < self.cols and 0 <= n_y < self.rows:
                # Add the index to the list of adjacent vectors
                adjacent_vectors.append(index)
        
        # Return the list of indices of adjacent vectors
        return adjacent_vectors
    
    def generate_moves(self, layers):
        # List to store all the move offsets
        moves = []
    
        # Iterate through each layer
        for i in range(-layers, layers + 1):
            for j in range(-layers, layers + 1):
                # Exclude the center point (0, 0) itself
                if i != 0 or j != 0:
                    # Append the offset (i, j) to the moves list
                    moves.append((i, j))
    
        # Return the list of moves
        return moves
    
    # Main method to run the vector field
    def run(self):
        # Clear existing forces and animate new ones
        #self.all_forces = []
        #self.animate_vecfield()
        # Display all forces
        self.display()

    # Display all forces in the field
    def display(self):
       println(len(self.all_forces))  # Print the number of forces (for debugging)
       for f in self.all_forces:
            f.run()  # Run each force (presumably to display it)
            
    def display_highlight(self, h_size):
        stroke(255)
        noFill()
        rectMode(CENTER)
        rect(self.pos.x, self.pos.y, h_size, h_size)
