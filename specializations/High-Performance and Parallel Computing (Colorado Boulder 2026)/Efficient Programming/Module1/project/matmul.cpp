#include <cstdlib>
#include <iostream>
#include <iomanip>
#include <cmath>
#include <chrono>
#include <cstdlib>
#include "cblas.h"

#include "array.hpp" // using the array lite library https://www.cs.cornell.edu/~saeed/lite/html/group__array__class.html

using namespace std;

typedef lite::array<double[1][1]> matrix; // matrix type with variable dimensions

int main(int argc, char *argv[]);
void init_matrix(matrix &a, int &seed);
std::pair<double, double> jik_matmul(matrix &a, matrix &b, matrix &c);
std::pair<double, double> lib_matmul(matrix &a, matrix &b, matrix &c);
std::pair<double, double> dgemm_matmul(matrix &a, matrix &b, matrix &c);

//
// A and B are real double precision matrices whose entries
// are assigned randomly. This version uses the array lite array library
//
int main(int argc, char *argv[])

{
    int n1 = 1000, n2 = 1000, n3 = 1000;
    double flops = 2.0 * (double)n1 * (double)n2 * (double)n3;

    std::cout << "\n";
    std::cout << "  Matrix A(" << n1 << ", " << n2 << ")" << std::endl;
    std::cout << "  Matrix B(" << n2 << ", " << n3 << ")" << std::endl;
    std::cout << "  Matrix C(" << n1 << ", " << n3 << ")" << std::endl;
    std::cout << "  Number of floating point operations = " << flops << std::endl;

    // Size of the matrices
    matrix A(n1, n2);
    matrix B(n2, n3);
    matrix C(n1, n3);
    //
    //  Set A and B with random numbers
    //
    int seed = 1325;
    init_matrix(A, seed);
    init_matrix(B, seed);

    std::cout << std::endl;
    std::cout << "  Method   Walltime [s]   MFLOPS          Checksum" << std::endl;
    std::cout << "  ------  --------------  --------------  --------------" << std::endl;

    //
    //  JIK
    //
    auto result_jik = jik_matmul(A, B, C);
    double wall_time_seconds = result_jik.first;
    double checksum = result_jik.second;
    double mflops = (double)(flops) / wall_time_seconds / 1000000.0;

    std::cout << "  JIK   " << fixed << setprecision(2)
              << "  " << setw(14) << wall_time_seconds
              << "  " << setw(14) << mflops
              << "  " << setw(14) << checksum << std::endl;

    //
    //  Library
    //
    auto result_lib = lib_matmul(A, B, C);
    wall_time_seconds = result_lib.first;
    checksum = result_lib.second;
    mflops = (double)(flops) / wall_time_seconds / 1000000.0;

    std::cout << "  Lib   "
              << "  " << setw(14) << wall_time_seconds
              << "  " << setw(14) << mflops
              << "  " << setw(14) << checksum << std::endl;
    //
    // DGEMM
    //
    auto result_dgemm = dgemm_matmul(A, B, C);
    wall_time_seconds = result_dgemm.first;
    checksum = result_dgemm.second;
    mflops = (double)(flops) / wall_time_seconds / 1000000.0;

    std::cout << "  DGEMM "
              << "  " << setw(14) << wall_time_seconds
              << "  " << setw(14) << mflops
              << "  " << setw(14) << checksum << std::endl;

    A.release();
    B.release();
    C.release();

    return 0;
}

// initialize matrix with a fixed seed
void init_matrix(matrix &a, int &seed)
{
    int n1 = a.size().i0;
    int n2 = a.size().i1;

    //
    //  Set the matrix a.
    //
    srand(seed);
    for (int j = 0; j < n2; j++)
        for (int i = 0; i < n1; i++)
        {
            a(j, i) = (double)(rand() % 1000) + 1;
        }
}

//
// JIK
std::pair<double, double> jik_matmul(matrix &a, matrix &b, matrix &c)
{
    auto asize = a.size();
    auto bsize = b.size();
    int n1 = asize.i0;
    int n2 = asize.i1;
    int n3 = bsize.i1;

    c = 0.0;

    auto start = std::chrono::steady_clock::now();

    for (int j = 0; j < n3; j++)
        for (int i = 0; i < n1; i++)
            for (int k = 0; k < n2; k++)
            {
                c(i, j) = c(i, j) + a(i, k) * b(k, j);
            }

    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> wall_seconds = end - start;

    double checksum = c(0, 0) + c(n1 - 1, n3 - 1);

    return {wall_seconds.count(), checksum};
}

//
// Lib using the built in array class matrixmultiply
std::pair<double, double> lib_matmul(matrix &a, matrix &b, matrix &c)
{
    auto asize = a.size();
    auto bsize = b.size();
    int n1 = asize.i0;
    int n2 = asize.i1;
    int n3 = bsize.i1;
    c = 0.0;

    auto start = std::chrono::steady_clock::now();

    c = a * b;

    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> wall_seconds = end - start;

    double checksum = c(0, 0) + c(n1 - 1, n3 - 1);

    return {wall_seconds.count(), checksum};
}

// TODO: Complete this function to use OpenBLAS
// dgemm
std::pair<double, double> dgemm_matmul(matrix &a, matrix &b, matrix &c)
{

    // Get matrix sizes
    auto asize = a.size();
    auto bsize = b.size();
    int n1 = asize.i0; // rows of A and C
    int n2 = asize.i1; // cols of A / rows of B
    int n3 = bsize.i1; // cols of B and C
    c = 0.0; 
    
    // Set scalar multipliers for DGEMM
    double alpha = 1.0; // multiplier for A*B
    double beta = 0.0;  // multiplier for C (we'll overwrite C)

    auto start = std::chrono::steady_clock::now();
    
    // TODO: Call cblass dgemm to perform the matrix multiplication
    cblas_dgemm(CblasColMajor, CblasNoTrans, CblasNoTrans,
                n1, n3, n2, alpha, a.data(), n3, b.data(), n2, beta, c.data(), n1);

    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> wall_seconds = end - start;

    double checksum = c(0,0) + c(n1-1, n3-1); 

    return {wall_seconds.count(), checksum};
}
