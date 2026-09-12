#!/bin/bash

# TODO: Compile the C++ program with optimization flags 
g++ -fopenmp -o sumSquaresParallel sumSquaresParallel.cpp
#g++ -O3 -fopenmp -fsimd-cost-model=unlimited -o sumSquaresParallel sumSquaresParallel.cpp

# Measure start time
start=$(date +%s.%N)

# TODO: Execute the program with GNU Parallel
##ml parallel
parallel -j+0 ./sumSquaresParallel :::: data.txt

# Measure end time
end=$(date +%s.%N)

# Calculate and print execution time
echo "Execution time: $(echo "$end - $start" | bc) seconds"
