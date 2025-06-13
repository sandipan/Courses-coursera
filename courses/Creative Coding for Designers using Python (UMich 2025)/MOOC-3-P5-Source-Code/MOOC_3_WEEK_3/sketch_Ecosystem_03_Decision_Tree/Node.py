class Node:
    
    def __init__(self, name =None, action=None, yesNode=None, noNode=None, condition=None, condition_var=None):
        # Initialize Node attributes
        self.name = name  # Store the name of the node
        self.action = action  # Store the action of the node
        self.yesNode = yesNode  # Store the reference to the "yes" child node
        self.noNode = noNode  # Store the reference to the "no" child node
        self.condition = condition  # Store the condition of the node
        self.condition_var = condition_var  # Store the condition variable of the node
    
    def message(self):
        # Print the name of the node
        println(self.name)
