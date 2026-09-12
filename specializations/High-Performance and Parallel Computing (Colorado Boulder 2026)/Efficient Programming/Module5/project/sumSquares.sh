#!/bin/bash

# Compile the C++ program
g++ -o sumSquares sumSquares.cpp

# Measure start time
start=$(date +%s.%N)

# Execute the program with the provided filename
./sumSquares data.txt

# Measure end time
end=$(date +%s.%N)

# Calculate and print execution time
echo "Execution time: $(echo "$end - $start" | bc) seconds"
