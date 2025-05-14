import pandas as pd
import json
import os

notebook_path = os.path.abspath(os.getcwd())
notebook_path = os.path.dirname(notebook_path)
print(notebook_path)
data_path = os.path.join(notebook_path,'Data\\financial-statement-symbol-lists.json')
print (data_path)
with open(data_path) as file:
    availableTickers = json.load(file)



print(len(availableTickers))