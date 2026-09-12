#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstring>
#include <unistd.h>
#include <chrono>
#include <cmath>
#include <ctime>

void tiled_matrix_multiply(double* A, double* B, double* C, int N, int tile_size) {
   for (int i = 0; i < N * N; ++i)
        C[i] = 0.0;

    //TODO: Implement Tiled Matrix Multiplication Here
   for (int i = 0; i < N; i += tile_size)
   {
       for (int j = 0; j < N; j += tile_size)
       {
           for (int k = 0; k < N; k += tile_size)
           {
               for (int ti = i; ti < std::min(i + tile_size, N); ++ti)
               {
                   for (int tk = k; tk < std::min(k + tile_size, N); ++tk)
                   {
                       for (int tj = j; tj < std::min(j + tile_size, N); ++tj)
                       {
                           C[ti * N + tj] += A[ti * N + tk] * B[tk * N + tj];
                       }
                   }
               }
           }
       }
    }
   
}

void matrix_multiply(double *A, double *B, double *C, int N) {
    for (int i = 0; i < N * N; ++i)
        C[i] = 0.0;

    for (int i = 0; i < N; ++i) {       
        for (int j = 0; j < N; ++j) {   
            for (int k = 0; k < N; ++k) {
                C[i*N + j] += A[i*N + k] * B[k*N + j];
            }
        }
    }
}

void initialize_matrices(double* A, double* B, int M, int N) {
    srand(time(NULL));

    // Initialize matrix A with random values
    for (int i = 0; i < M * N; i++) {
        A[i] = static_cast<double>(rand()) / RAND_MAX;
    }

    // Initialize matrix B with random values
    for (int i = 0; i < M * N; i++) {
        B[i] = static_cast<double>(rand()) / RAND_MAX;
    }
}

// DO NOT EDIT - EDITING OUTPUT FILE FORMAT MAY IMPACT GRADING 
int main() {
    const int M = 1024, N = 1024;
    double* A = new double[M * N];
    double* B = new double[M * N];
    double* C = new double[M * N];

    // Initialize matrices A and B with some values
    initialize_matrices(A, B, M, N);

    // Measure execution time for native implementation
    auto native_start = std::chrono::high_resolution_clock::now();
    matrix_multiply(A, B, C, N);
    auto native_end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> native_elapsed = native_end - native_start;
    std::cout << "Non-tiled execution time: " << native_elapsed.count() << " seconds" << std::endl;
    std::cout << "Verification checksum: " << C[0] + C[M*N-1] << std::endl; 
    std::cout << std::endl;

    const int cache_sizes[] = {64 * 1024, 128 * 1024, 256 * 1024, 1024 * 1024}; // Sizes in bytes

    for (size_t i = 0; i < sizeof(cache_sizes) / sizeof(cache_sizes[0]); ++i) {
        int tile_size = static_cast<int>(std::sqrt(cache_sizes[i] / (8 * (2 * M + N))));
        std::cout << "Cache size: " << cache_sizes[i] / 1024 << " KB" << std::endl;
        std::cout << "Tile size: " << tile_size << std::endl;

        // Measure execution time for tiled implementation
        auto start = std::chrono::high_resolution_clock::now();
        tiled_matrix_multiply(A, B, C, N, tile_size);
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = end - start;
        std::cout << "Tiled execution time: " << elapsed.count() << " seconds" << std::endl;
        std::cout << "Verification checksum: " << C[0] + C[M*N-1] << std::endl; 
        std::cout << std::endl;
    }


    delete[] A;
    delete[] B;
    delete[] C;

    return 0;
}