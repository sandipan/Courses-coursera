#include <iostream>
#include <chrono>
#include <vector>
#include <omp.h>
#include <cstdlib>
#include <ctime>
#include <cstring>

// Function to perform dot product of two arrays
double dotProduct(double* a, double* b, std::size_t size) {
    double result = 0.0;
    for (std::size_t i = 0; i < size; ++i) {
        result += a[i] * b[i];
    }
    return result;
}

// TODO: Function to perform dot product of two vectors
double vectorizedDotProduct(double* aligned_a, double* aligned_b, std::size_t size) {
    double result_vectorized = 0.0;
    // TODO
    #pragma omp simd reduction(+:result_vectorized)
    for (std::size_t i = 0; i < size; ++i) {
        result_vectorized += aligned_a[i] * aligned_b[i];
    }
    return result_vectorized;
}


int main() {
    const std::size_t arraySize = 10000000; // Array size of 10^7
    std::vector<double> a(arraySize), b(arraySize);

    // Initialize arrays a and b with random values
    std::srand(std::time(nullptr));
    for (std::size_t i = 0; i < arraySize; ++i) {
        a[i] = static_cast<double>(std::rand()) / RAND_MAX;
        b[i] = static_cast<double>(std::rand()) / RAND_MAX;
    }

    // Measure execution time for unaligned dot product
    auto start = std::chrono::high_resolution_clock::now();
    double result_unaligned = dotProduct(a.data(), b.data(), arraySize);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Execution time (unaligned): " << elapsed.count() << " seconds" << std::endl;

    // Allocate aligned memory for a and b, and call dotProduct with aligned arrays
    double* aligned_a = nullptr;
    double* aligned_b = nullptr;
    posix_memalign(reinterpret_cast<void**>(&aligned_a), 64, arraySize * sizeof(double));
    posix_memalign(reinterpret_cast<void**>(&aligned_b), 64, arraySize * sizeof(double));
    memcpy(aligned_a, a.data(), arraySize * sizeof(double));
    memcpy(aligned_b, b.data(), arraySize * sizeof(double));

    // Vectorize the dot product loop using OpenMP SIMD
    start = std::chrono::high_resolution_clock::now();
    double result_aligned_vectorized = vectorizedDotProduct(aligned_a, aligned_b, arraySize);
    end = std::chrono::high_resolution_clock::now();
    elapsed = end - start;
    std::cout << "Execution time (vectorized with OpenMP): " << elapsed.count() << " seconds" << std::endl;

    // Verify the results
    std::cout << "Result (unaligned): " << result_unaligned << std::endl;
    std::cout << "Result (aligned, vectorized): " << result_aligned_vectorized << std::endl;

    free(aligned_a);
    free(aligned_b);

    return 0;
}
