## Assignment Instructions

In this assignment, you will implement a parallel version of a program that calculates the sum of squares from 1 to N, where N is a large number read from a data file. You will compare the performance of the parallel implementation against the sequential version.


### Part 1: Sequential Implementation
The following files are provided:
   - sumSquares.cpp - C++ code to calculate the sum of squares sequentially
   - sumSquares.sh - Bash script to compile and run sumSquares.cpp, measuring execution time

Run the sequential implementation: ./sumSquares.sh

Observe the execution time printed by the script.

### Part 2: Parallel Implementation
1. Edit the C++ file `sumSquaresParallel.cpp` and implement the parallel version of the `sumOfSquares` function using OpenMP parallelization. Use the `#pragma omp parallel for` directive to parallelize the loop and the `reduction(+:sum)` clause to perform the reduction operation correctly.
2. Create a new bash script `sumSquaresParallel.sh` that:
    - Compiles the `sumSquaresParallel.cpp` file with OpenMP support
    - Reads the data file (`data.txt`) containing numbers on separate lines
    - Runs the `sumSquaresParallel` executable for each number in the data file, using GNU Parallel 
    - Measures and prints the total execution time


**Hint: To run the executable for each line in the data file using GNU Parallel try something like `parallel -j+0`**

Run the parallel implementation: ./sumSquaresParallel.sh
Observe the execution time printed by the script.

### Submission: 
Upload a compressed file (as .tar), containing:
    - sumSquaresParallel.cpp
    - sumSquaresParallel.sh


Compare the execution times of the sequential and parallel implementations. Analyze the performance improvement achieved by parallelization and identify any potential bottlenecks or limitations.

**Note: The provided data file `data.txt` contains large numbers for which the sum of squares calculation is computationally intensive, making it suitable for parallelization.**
