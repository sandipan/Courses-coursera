#include <iostream>
#include <sstream>

// Function to calculate the sum of squares from 1 to N
unsigned long long sumOfSquares(unsigned long long N) {
    unsigned long long sum = 0;
    // TODO: parallelization
    #pragma omp parallel for reduction(+:sum)
    for (unsigned long long i = 1; i <= N; ++i) {
        sum += i * i;
    }
    return sum;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <number>" << std::endl;
        return 1;
    }

    // Convert the input argument to a number
    std::istringstream iss(argv[1]);
    unsigned long long number;
    if (!(iss >> number)) {
        std::cerr << "Invalid number: " << argv[1] << std::endl;
        return 1;
    }

    // Calculate the sum of squares for the given number
    unsigned long long result = sumOfSquares(number);
    std::cout << "Result for " << number << ": " << result << std::endl;

    return 0;
}
