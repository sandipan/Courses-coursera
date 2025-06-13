
import random
from Tiles import Tile

class Environment:
    
    def __init__(self, cols, rows, world_x, world_y):
        self.cols = cols
        self.rows = rows
        self.world_x = world_x
        self.world_y = world_y
        self.cells = []
        
        self.init_cells()
        
        self.running = False
        self.path_found = False
        self.start_node = None
        self.end_node = None
        self.stack = []
        self.path = []
        
        self.start_node = self.get_cell(100,100)
        self.end_node = self.get_cell(1000,400)
        self.stack.append(self.start_node)
        
        
    
    def run(self):
        self.run_tiles()
        self.draw_visited()
        self.draw_stack()
        self.draw_path()
        self.draw_start()
        self.draw_end()
        self.flood_fill()
    
    def draw_start(self):
        col = color(255,0,0)
        self.start_node.display_highlight(col)
    
    def draw_end(self):
        col = color(0,255,0)
        self.end_node.display_highlight(col)
    
    def draw_stack(self):
        col = color(0,255,255)
        for cell in self.stack:
            cell.display_highlight(col)
            
    def draw_visited(self):
        col = color(0,0,255)
        for column in self.cells:
            for cell in column:
                if cell.visited:
                    cell.display_highlight(col)
                    
    def draw_path(self):
        if self.path_found:
            col = color(255,0,255)
            for cell in self.path:
                cell.display_highlight(col)
    
    def flood_fill(self):
        if self.running:        
            if len(self.stack) > 0:
                current_cell = self.stack.pop(0) # we remove the last element and assign it to the variable
                current_cell.visited = True
                
                if current_cell == self.end_node:
                    println("Goal Reached!")
                    self.running = False
                    self.path_found = True
                    self.reconstruct_path(current_cell)
            
                for neighbor in current_cell.get_neighbors():
                    if not neighbor.visited and not neighbor.isObstable:
                        neighbor.visited = True
                        self.stack.append(neighbor)
                        neighbor.parent = current_cell
                        
    def reconstruct_path(self, current_cell):
        println("Reconstruction Started")
        while current_cell.parent is not None:
            self.path.append(current_cell)
            current_cell = current_cell.parent
            println("Loop")
            
        self.path.append(self.start_node)
        println("Reconstruction Ended")
    
    
            
    def draw_neighbors(self, x, y):

        cell = self.get_cell(x,y)
        col = color(255,0,0)
        cell.display_highlight(col)
        
        neighbors = cell.get_neighbors()
        for n in neighbors:
            col = color(0,0,255)
            n.display_highlight(col)
    
    def run_tiles(self):
        for column in self.cells:
            for cell in column:
                cell.run()
                
    def init_cells(self):
        
        cell_size = float(self.world_x) / self.cols
        #println(cell_size)
        for i in range(self.cols):
            self.cells.append([])
            for j in range (self.rows):
                pos = PVector(i*cell_size, j * cell_size)
                new_tile = Tile(pos, cell_size, 0,self.cols, self.rows, i, j, self.cells)
                self.cells[i].append(new_tile)
    
    
    def paint_cell(self, x, y, type):
        #println(str(x) + "," + str(y) + "," + str(type) )
        cell = self.get_cell(x,y)
        if(cell is not None):
            #cell.current_type = type
            cell.change_type(type)
      
    def get_cell(self,x,y):
        
        x = int( x / (float(self.world_x) / self.cols)  )
        y = int( y / (float(self.world_y) / self.rows)  )
        
        if (x < len (self.cells)  and y < len(self.cells[0]) ):
            cell = self.cells[x][y]
            return cell
        else:
            return None
    
       
            
        
        

        
    
