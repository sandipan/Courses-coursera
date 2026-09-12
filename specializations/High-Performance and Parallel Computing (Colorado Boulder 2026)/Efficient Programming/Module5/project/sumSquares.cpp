#include <iostream>
#include <fstream>
#include <string>

// Function to calculate the sum of squares from 1 to N
unsigned long long sumOfSquares(unsigned long long N) {
    unsigned long long sum = 0;
    for (unsigned long long i = 1; i <= N; ++i) {
        sum += i * i;
    }
    return sum;
}

// Function to process a single file
void processFile(const std::string& filename) {
    std::ifstream file(filename);
    if (file.is_open()) {
        long long N;
        while (file >> N) {
            unsigned long long result = sumOfSquares(N);
            std::cout << "Result for " << filename << " (N = " << N << "): " << result << std::endl;
        }
        file.close();
        file >> N;
    } else {
        std::cerr << "Unable to open file: " << filename << std::endl;
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
        return 1;
    }

    std::string filename = argv[1];
    processFile(filename);

    return 0;
}
