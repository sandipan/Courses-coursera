import random  # Import the random module.
from Tiles import Tile  # Import the Tile class.

class Environment:
    
    def __init__(self, cols, rows, world_x, world_y):
        # Initialize the environment with its dimensions and create a cell grid.
        self.cols = cols  # Number of columns in the grid.
        self.rows = rows  # Number of rows in the grid.
        self.world_x = world_x  # Width of the environment.
        self.world_y = world_y  # Height of the environment.
        self.cells = []  # 2D list to hold cell objects.
        
        self.init_cells()  # Populate the cells with Tile objects.
        
        # Variables for pathfinding or traversal.
        self.start_node = None  # Starting node for pathfinding.
        self.end_node = None  # Ending node for pathfinding.
        self.stack = []  # Stack for traversal/pathfinding.
        
    
    def run(self):
        # Update each cell in the environment.
        self.run_tiles()
        # Uncomment to print the number of cells.
        #println(len(self.cells))
    
    def draw_neighbors(self, x, y):
        # Highlight a cell and its neighbors.
        cell = self.get_cell(x, y)  # Get the cell at x, y.
        col = color(255, 0, 0)  # Red color for the selected cell.
        cell.display_highlight(col)  # Highlight the selected cell.
        
        neighbors = cell.get_neighbors()  # Get the neighboring cells.
        for n in neighbors:
            col = color(0, 0, 255)  # Blue color for neighbors.
            n.display_highlight(col)  # Highlight each neighbor.
    
    def run_tiles(self):
        # Call the run method on each Tile object in the cells grid.
        for column in self.cells:
            for cell in column:
                cell.run()
                
    def init_cells(self):
        # Calculate cell size based on the environment size and number of cells.
        cell_size = float(self.world_x) / self.cols
        # Uncomment to print the size of each cell.
        #println(cell_size)
        for i in range(self.cols):  # For each column...
            self.cells.append([])  # Add a new list for the column.
            for j in range(self.rows):  # For each row...
                pos = PVector(i*cell_size, j*cell_size)  # Position of the cell.
                # Create a new Tile object and add it to the column.
                new_tile = Tile(pos, cell_size, 0, self.cols, self.rows, i, j, self.cells)
                self.cells[i].append(new_tile)
    
    
    def paint_cell(self, x, y, type):
        # Change the type of a cell at x, y coordinates.
        # Uncomment to print the coordinates and type.
        #println(str(x) + "," + str(y) + "," + str(type))
        cell = self.get_cell(x, y)  # Get the cell.
        if(cell is not None):  # If the cell exists...
            cell.current_type = type  # Update the cell's type.
      
    def get_cell(self, x, y):
        # Calculate grid indices based on x, y coordinates.
        x = int(x / (float(self.world_x) / self.cols))
        y = int(y / (float(self.world_y) / self.rows))
        
        # Check if the indices are within bounds and return the cell if so.
        if (x < len(self.cells) and y < len(self.cells[0])):
            cell = self.cells[x][y]
            return cell
        else:
            return None  # Return None if the indices are out of bounds.
