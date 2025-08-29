#!/bin/bash
echo "Running your code..."
/home/coder/miniconda/bin/python3 poker.py > output.txt
echo "Checking the output..."
/home/coder/miniconda/bin/python3 check_output.py
