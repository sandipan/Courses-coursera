import random  # Import the random module for generating random values
from Node import Node  # Import the Node class from the Node module

class Herbivore:
    
    def __init__ (self, pos, all_food, all_herbivores):
        self.pos = pos  # Set the position of the herbivore
        self.vel = PVector(random.uniform(-0.5,0.5),random.uniform(-0.5,0.5))  # Set the velocity of the herbivore
        self.isAwake = True  # Set the herbivore's initial state as awake
        self.isHungry = False  # Set the herbivore's initial state as not hungry
        self.isTired = False  # Set the herbivore's initial state as not tired
        self.current_node = self.build_decision_tree()  # Set the initial decision node of the herbivore
        self.hunger_level = 0  # Initialize the hunger level of the herbivore
        self.hunger_threshold = 400  # Set the hunger threshold of the herbivore
        self.rest_level = 0  # Initialize the rest level of the herbivore
        self.rest_threshold = 100  # Set the rest threshold of the herbivore
        
        self.wander_states = ("IDLE","MOVING","ROTATING")  # Define the possible wander states
        self.current_wander_state = 0  # Initialize the current wander state
        self.action_duration = 200  # Set the duration of each action
        self.action_count = 0  # Initialize the action count
        
        self.all_foods = all_food  # Store all food objects in the environment
        self.all_herbivores = all_herbivores  # Store all herbivore objects in the environment
        
        self.starvation_value = 0  # Initialize the starvation value of the herbivore
        self.starvation_threshold = 400  # Set the starvation threshold

    def run(self):
        # Execute the herbivore's behavior
        self.display()
        self.display_behavior()
        self.current_node.message()
        self.update_current_node()
        
    def update_current_node(self):
        # Update the current decision node based on conditions and actions
        if self.current_node.condition_var is not None:  # EVALUATE CONDITION NODES FIRST
            if self.current_node.condition_var:
                self.current_node = self.current_node.yesNode
            else: 
                self.current_node = self.current_node.noNode
        elif self.current_node.action is not None:  # EVALUATE ACTION NODES
            #println("Animal will: " + self.current_node.action)
            self.current_node.action_func()

            
            
    def build_decision_tree(self):
        # Construct the decision tree for herbivore behavior
        leaf1 = Node(name="l1", action="Wander", action_func=self.wander)
        leaf2 = Node(name="l2", action="Seek Food", action_func=self.seek_food)
        leaf3 = Node(name="l3", action="Rest", action_func=self.rest)
        
        node1 = Node(name="n1", condition="Is Hungry?", yesNode=leaf2, noNode=leaf1, condition_var=self.isHungry)
        #node2 = Node(name="n2", condition="Is Tired?", yesNode=leaf3, noNode=leaf1, condition_var=self.isTired)
        
        root = Node(name="root", condition="Is Awake?", yesNode=node1, noNode=leaf3, condition_var=self.isAwake)
        
        return root
    
    def wander(self):
        # Execute wandering behavior
        #println("wandering, hunger: " + str(self.hunger_level) + "/" + str(self.hunger_threshold) + "," + str(self.isHungry) )
        self.wander_actions()
        self.hunger_level += 1
        if(self.hunger_level > self.hunger_threshold):
            self.isHungry = True
            self.current_node = self.build_decision_tree()

        
    def wander_actions(self):
        # Print the current wandering state and action count/duration
        println(self.wander_states[self.current_wander_state] + ", " + str(self.action_count) + "/" + str(self.action_duration) )
        # Check the current wandering state and perform corresponding action
        if(self.wander_states[self.current_wander_state]  == "IDLE"):
            #self.idle()
            self.trigger_action_change()  # Perform action change if in idle state
        elif(self.wander_states[self.current_wander_state]  == "MOVING"):
            self.move(0.5)  # Move with a certain speed
            self.trigger_action_change()  # Perform action change if moving
        elif(self.wander_states[self.current_wander_state]  == "ROTATING"):
            self.new_rotation()  # Rotate in a new direction
            self.next_wander_state()  # Move to the next wandering state
        else:
            println("No action")  # If no action is possible
    
    def idle(self):
        self.action_count += 1  # Increment the action count when idling
    
    def trigger_action_change(self):    
        self.action_count += 1  # Increment the action count
        # Check if action count exceeds duration, then change action
        if(self.action_count > self.action_duration):
            self.next_wander_state()  # Move to the next wandering state
            self.action_count = 0  # Reset the action count
            self.action_duration = random.randrange(150,250)  # Randomize the action duration
    
    
    def next_wander_state(self):
        # Move to the next wandering state, cycling back to 0 if exceeds the limit
        self.current_wander_state += 1
        if(self.current_wander_state > 2):
            self.current_wander_state = 0
    
    def new_rotation(self):
        # Generate a new random angle for rotation
        new_angle = random.uniform(0,360)
        # Rotate the velocity vector by the new angle
        self.vel = self.rotate_vector(self.vel, new_angle)
    
    def rotate_vector(self, v, angle):
        # Convert angle to radians
        angle = radians(angle)
        # Perform vector rotation
        x = v.x * cos(angle) - v.y * sin(angle)
        y = v.x * sin(angle) + v.y * cos(angle)
        return PVector(x, y)
    
    def rest(self):
        # Increment rest level
        self.rest_level += 1
        # Check if rest level exceeds threshold to wake up
        if(self.rest_level > self.rest_threshold):
            self.isAwake = True
            self.current_node = self.build_decision_tree()  # Rebuild decision tree after resting
            self.rest_level = 0  # Reset rest level
    
    def seek_food(self):
        #println("seeking food, starvation: " + str(self.starvation_value) + "/" + str(self.starvation_threshold) )
        
        # Find the closest food
        closest_food = self.find_closest_food()
        # Look towards the closest food
        self.look_towards(closest_food.vec_position)
        # Move towards the food
        self.move(1.5)
        # Eat food in range and transition back to not hungry and go to sleep
        self.eat_food_in_range(closest_food, 5)
        
        # Increment starvation value and check for starvation
        self.starvation_value += 1
        if(self.starvation_value > self.starvation_threshold):
            self.die()
    
    def die(self):
        # Remove the herbivore from the list
        self.all_herbivores.remove(self)
    
    def eat_food_in_range(self, closest_food, eat_range):
        # Calculate distance to the food
        diff = closest_food.vec_position.copy().sub(self.pos)
        distance = diff.mag()
        # If within eating range, eat the food
        if(distance < eat_range):
            closest_food.remove_self()
            self.hunger_level = 0
            self.isHungry = False
            self.isAwake = False
            self.current_node = self.build_decision_tree()
    
    def find_closest_food(self):
        # Find the closest food item among all available foods
        closest_dist = 10000000
        closest_id = -1
        for i, food in enumerate(self.all_foods):
            # Calculate distance to current food
            diff = self.pos.copy().sub(food.vec_position)
            distance = diff.mag()
            # Update closest food if closer
            if distance < closest_dist:
                closest_dist = distance
                closest_id = i
        # Retrieve the closest food
        closest_food = self.all_foods[closest_id] 
        # Draw a line to the closest food for visualization
        stroke(255, 50)   
        line(self.pos.x, self.pos.y, closest_food.vec_position.x, closest_food.vec_position.y)
                
        return closest_food
    
    def look_towards(self, target_vector):
        # Calculate the difference between the target and current position
        diff = target_vector.copy().sub(self.pos)
        current_magnitude = self.vel.mag()  # Get current velocity magnitude
        diff.normalize()  # Normalize the difference vector
        diff.mult(current_magnitude)  # Scale the difference vector
        
        # Set the velocity to the adjusted difference vector
        self.vel = diff

    def move(self, factor):
        # Normalize velocity vector and scale by given factor
        self.vel.normalize()
        self.vel.mult(factor)
        self.pos.add(self.vel)  # Move the object by the scaled velocity
    
    def display_behavior(self):
        
        #Hunger
        pushMatrix()
        translate(self.pos.x - 10, self.pos.y - 15)
        noStroke()
        fill(255)
        rect(0,0,20,3) #white background
        h = map(self.hunger_level, 0,self.hunger_threshold, 0, 20) #Map the hunger value to the size of the rectangle
        fill(0,0,255) #Blue
        rect(0,0,h,3) #draw rectangle as hunger meter
        popMatrix()
        
        #Rest
        pushMatrix()
        translate(self.pos.x - 10, self.pos.y - 20)
        noStroke()
        fill(255)
        rect(0,0,20,3) #white background
        r = map(self.rest_level, 0, self.rest_threshold, 0,20) #Map the rest value to the size of the rectangle
        fill(255,0,0) #Red
        rect(0,0,r,3) #draw rectangle as rest meter
        popMatrix()
        
        #Starvation
        pushMatrix()
        translate(self.pos.x - 10, self.pos.y - 25)
        noStroke()
        fill(255)
        rect(0,0,20,3) #white background
        s = map(self.starvation_value, 0, self.starvation_threshold, 0,20) #Map the starvation value to the size of the rectangle
        fill(0,255,0) #Green
        rect(0,0,s,3) #draw rectangle as starvation meter
        popMatrix()
        
    def display(self):
        # Draw the object
        noStroke()  # No outline
        fill(100, 50, 100)  # Fill color
        ellipse(self.pos.x, self.pos.y, 8, 8)  # Draw an ellipse
        
        # Draw a directional arrow
        stroke(255)  # Arrow color
        pushMatrix()  # Save the current transformation matrix
        translate(self.pos.x, self.pos.y)  # Translate to the object's position
        angle = self.get_angle(self.vel)  # Get the angle of the velocity vector
        rotate(angle)  # Rotate by the angle
        arrow_size = 10  # Size of the arrow
        line(0, 0, arrow_size, 0)  # Draw the line of the arrow
        line(arrow_size, 0, arrow_size - 5, 5)  # Draw the first segment of the arrow
        line(arrow_size, 0, arrow_size - 5, -5)  # Draw the second segment of the arrow
        popMatrix()  # Restore the previous transformation matrix

    def get_angle(self, vec):
        # Calculate the angle of the vector
        return atan2(vec.y, vec.x)  # Return the angle using atan2
    
