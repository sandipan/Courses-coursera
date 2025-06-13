from Food import Food 
from Herbivore import Herbivore
import random

class World_Manager:
    
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.all_food = []
        self.all_herbivores = []
        
        x = 600
        y = 300
        pos = PVector(x,y)
        new_herbivore = Herbivore(pos, self.all_food)
        self.all_herbivores.append(new_herbivore)
    
    def create_food(self, rate):
        if(frameCount % rate == 0):
            x = random.randrange(0,self.size_x)
            y = random.randrange(0,self.size_y)
            pos = PVector(x,y)
            new_food = Food(pos, 5, self.all_food)
            self.all_food.append(new_food)
    
    def create_herbivore(self, rate):
        if(frameCount % rate == 0):
            x = random.randrange(0,self.size_x)
            y = random.randrange(0,self.size_y)
            pos = PVector(x,y)
            new_herbivore = Herbivore(pos, self.all_food)
            self.all_herbivores.append(new_herbivore)
        
    
    def run(self):
        self.create_food(50)
        #self.create_herbivore(120)
        self.run_food()
        self.run_herbivores()
        
    def run_food(self):
        for f in self.all_food:
            f.run()
    
    def run_herbivores(self):
        for h in self.all_herbivores:
            h.run()
        
    
