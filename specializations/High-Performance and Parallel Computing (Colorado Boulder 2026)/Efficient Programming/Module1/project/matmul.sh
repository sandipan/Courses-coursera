#!/bin/bash

# === Compiler and Flags ===
CXX=g++
CXXFLAGS="-Ofast -pg"
EXTRA_FLAGS="-DLITE_ARRAY_NO_HINT -DNDEBUG"

# === OpenBLAS Paths ===
OPENBLAS_INCLUDE="/usr/include/openblas"
OPENBLAS_LIB="/usr/lib"

# === Output and Source Files ===
SOURCE_FILE="matmul.cpp"
OUTPUT_FILE="matmul"

# === TODO: Complete and add the correct flags ===
# Hint:
# 1. Add profiling support
# 2. Add OpenBLAS paths
# 4. Link against OpenBLAS

$CXX $CXXFLAGS $EXTRA_FLAGS $SOURCE_FILE -o $OUTPUT_FILE -lopenblas -L$OPENBLAS_LIB

# Execute the program and output the results to data.txt
./$OUTPUT_FILE > data.txt

# === TODO: Generate the profiling report ===
# Hint:
# - Use `gprof` to analyze the program's profiling data
# - The compiled executable is `./matmul`
# - The profiling data file is `gmon.out`
# - Redirect the output to a file named `profile_report.txt`
gprof ./$OUTPUT_FILE gmon.out > profile_report.txt