from Food import Food  # Import the Food class from the Food module
from Herbivore import Herbivore  # Import the Herbivore class from the Herbivore module
import random  # Import the random module for generating random values

class World_Manager:
    
    def __init__(self, size_x, size_y):
        self.size_x = size_x  # Initialize the width of the world
        self.size_y = size_y  # Initialize the height of the world
        self.all_food = []  # Initialize the list to store all food instances
        self.all_herbivores = []  # Initialize the list to store all herbivore instances
        
        x = random.randrange(0,self.size_x)  # Generate a random x-coordinate for herbivore spawn
        y = random.randrange(0,self.size_y)  # Generate a random y-coordinate for herbivore spawn
        pos = PVector(x,y)  # Create a position vector for the herbivore
        new_herbivore = Herbivore(pos)  # Create a new herbivore instance at the generated position
        self.all_herbivores.append(new_herbivore)  # Add the new herbivore to the list
    
    def create_food(self, rate):
        # Create food at a certain rate
        if(frameCount % rate == 0):  # Check if the frame count matches the rate
            x = random.randrange(0,self.size_x)  # Generate a random x-coordinate for food spawn
            y = random.randrange(0,self.size_y)  # Generate a random y-coordinate for food spawn
            pos = PVector(x,y)  # Create a position vector for the food
            new_food = Food(pos, 5, self.all_food)  # Create a new food instance at the generated position
            self.all_food.append(new_food)  # Add the new food to the list
    
    def create_herbivore(self, rate):
        # Create herbivores at a certain rate
        if(frameCount % rate == 0):  # Check if the frame count matches the rate
            x = random.randrange(0,self.size_x)  # Generate a random x-coordinate for herbivore spawn
            y = random.randrange(0,self.size_y)  # Generate a random y-coordinate for herbivore spawn
            pos = PVector(x,y)  # Create a position vector for the herbivore
            new_herbivore = Herbivore(pos)  # Create a new herbivore instance at the generated position
            self.all_herbivores.append(new_herbivore)  # Add the new herbivore to the list
    
    def run(self):
        self.create_food(50)  # Create food at a rate of 50
        self.create_herbivore(120)  # Create herbivores at a rate of 120
        self.run_food()  # Execute the run_food function
        self.run_herbivores()  # Execute the run_herbivores function
        
    def run_food(self):
        # Run all food instances
        for f in self.all_food:  # Iterate through all food instances
            f.run()  # Execute the run function of each food instance
    
    def run_herbivores(self):
        # Run all herbivore instances
        for h in self.all_herbivores:  # Iterate through all herbivore instances
            h.run()  # Execute the run function of each herbivore instance
