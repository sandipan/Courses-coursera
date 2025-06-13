from Food import Food  # Import the Food class from the Food module
from Herbivore import Herbivore  # Import the Herbivore class from the Herbivore module
import random  # Import the random module for generating random values

class World_Manager:
    
    def __init__(self, size_x, size_y):
        # Initialize the world manager with given size
        self.size_x = size_x
        self.size_y = size_y
        self.all_food = []  # List to store all food objects
        self.all_herbivores = []  # List to store all herbivore objects
        
        # Initialize a herbivore at a fixed position
        x = 600
        y = 300
        pos = PVector(x, y)
        new_herbivore = Herbivore(pos, self.all_food, self.all_herbivores)
        self.all_herbivores.append(new_herbivore)
    
    def create_food(self, rate):
        # Create new food objects at a given rate
        if(frameCount % rate == 0):
            x = random.randrange(0, self.size_x)
            y = random.randrange(0, self.size_y)
            pos = PVector(x, y)
            new_food = Food(pos, 5, self.all_food)
            self.all_food.append(new_food)
    
    def create_herbivore(self, rate):
        # Create new herbivore objects at a given rate
        if(frameCount % rate == 0):
            x = random.randrange(0, self.size_x)
            y = random.randrange(0, self.size_y)
            pos = PVector(x, y)
            new_herbivore = Herbivore(pos, self.all_food, self.all_herbivores)
            self.all_herbivores.append(new_herbivore)
        
    def run(self):
        # Run the simulation
        self.create_food(20)
        self.create_herbivore(80)
        self.run_food()
        self.run_herbivores()
        
    def run_food(self):
        # Run the food objects
        for f in self.all_food:
            f.run()
    
    def run_herbivores(self):
        # Run the herbivore objects
        for h in self.all_herbivores:
            h.run()
