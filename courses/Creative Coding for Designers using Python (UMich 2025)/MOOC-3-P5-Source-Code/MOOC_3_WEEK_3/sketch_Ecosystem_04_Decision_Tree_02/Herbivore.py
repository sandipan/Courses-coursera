import random  # Import the random module for generating random values
from Node import Node  # Import the Node class from the Node module

class Herbivore:
    
    def __init__ (self, pos):
        self.pos = pos  # Initialize the position of the Herbivore
        self.vel = PVector(random.uniform(-0.5,0.5),random.uniform(-0.5,0.5))  # Initialize the velocity of the Herbivore with random values
        self.isAwake = True  # Initialize the awake state of the Herbivore
        self.isHungry = False  # Initialize the hungry state of the Herbivore
        self.isTired = False  # Initialize the tired state of the Herbivore
        self.current_node = self.build_decision_tree()  # Initialize the decision tree of the Herbivore

    def run(self):
        self.move()  # Execute the move function to move the Herbivore
        self.display()  # Execute the display function to display the Herbivore
        self.current_node.message()  # Execute the message function of the current node in the decision tree
        self.update_current_node()  # Execute the update_current_node function to update the current node in the decision tree
    
    ############################################################    
    
    def update_current_node(self):
        # Update the current node based on conditions or actions
        if self.current_node.condition_var is not None:  # If the current node has a condition variable
            if self.current_node.condition_var:  # If the condition is true
                self.current_node = self.current_node.yesNode  # Move to the yesNode
            else: 
                self.current_node = self.current_node.noNode  # Move to the noNode
        elif self.current_node.action is not None:  # If the current node has an action
            println("Animal will: " + self.current_node.action)  # Print the action
            
    def build_decision_tree(self):
        # Build the decision tree for the Herbivore behavior
        leaf1 = Node(name="l1", action="Wander")  # Create a leaf node for wandering
        leaf2 = Node(name="l2", action="Seek Food")  # Create a leaf node for seeking food
        leaf3 = Node(name="l3", action="Rest")  # Create a leaf node for resting
        
        node1 = Node(name="n1", condition="Is Hungry?", yesNode=leaf2, noNode=leaf1, condition_var=self.isHungry)  # Create a condition node for hunger
        node2 = Node(name="n1", condition="Is Tired?", yesNode=leaf3, noNode=leaf1, condition_var=self.isTired)  # Create a condition node for tiredness
        
        root = Node(name="root", condition="Is Awake?", yesNode=node1, noNode=leaf3, condition_var=self.isAwake)  # Create the root node
        
        return root  # Return the root node of the decision tree
    ############################################################
    
    def move(self):
        # Move the Herbivore
        self.pos.add(self.vel)  # Update the position by adding the velocity
    
    def display(self):
        # Display the Herbivore
        noStroke()  # No stroke for drawing
        fill(100,50,100)  # Fill color for the Herbivore
        ellipse(self.pos.x, self.pos.y, 8, 8)  # Draw the Herbivore as an ellipse
        
        stroke(255)  # Stroke color for drawing
        pushMatrix()  # Push the current transformation matrix onto the stack
        translate(self.pos.x, self.pos.y)  # Translate to the position of the Herbivore
        angle = self.get_angle(self.vel)  # Get the angle of the velocity vector
        rotate(angle)  # Rotate by the angle
        arrow_size = 10  # Size of the arrow
        line(0,0,arrow_size,0)  # Draw the line of the arrow
        line(arrow_size,0,arrow_size-5,5)  # Draw the first segment of the arrow
        line(arrow_size,0,arrow_size-5,-5)  # Draw the second segment of the arrow
        popMatrix()  # Pop the current transformation matrix from the stack
    
    def get_angle(self, vec):
        # Calculate the angle of the vector
        return atan2(vec.y, vec.x)  # Return the angle using atan2
