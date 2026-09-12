#include <iostream>
#include <vector>
#include <numeric>
#include <mpi.h>

int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int ARRAY_SIZE = 1000;
    std::vector<int> global_array(ARRAY_SIZE);
    std::vector<int> partial_sums(size);

    if (rank == 0)
    {
        // Initialize the array with values 1 to 1000
        std::iota(global_array.begin(), global_array.end(), 1);
        std::cout << "Original array sum: " << std::accumulate(global_array.begin(), global_array.end(), 0) << std::endl;
    }

    // Calculate the chunk size for each process
    int chunk_size = ARRAY_SIZE / size;
    std::vector<int> local_array(chunk_size);

    // TODO: Implement MPI_Scatter to distribute the array
    // Scatter the array from rank 0 to all processes
    MPI_Scatter(global_array.data(), chunk_size, MPI_INT,
                local_array.data(), chunk_size, MPI_INT,
                0, MPI_COMM_WORLD);

    // Compute partial sum
    int partial_sum = std::accumulate(local_array.begin(), local_array.end(), 0);
    std::cout << "Process " << rank << " partial sum: " << partial_sum << std::endl;

    // TODO: Implement MPI_Gather to collect partial sums
    // Gather the partial sums from all processes to rank 0
    MPI_Gather(&partial_sum, 1, MPI_INT,
                partial_sums.data(), 1, MPI_INT,
                0, MPI_COMM_WORLD);

    if (rank == 0)
    {
        int final_sum = std::accumulate(partial_sums.begin(), partial_sums.end(), 0);
        std::cout << "Final sum: " << final_sum << std::endl;
    }

    MPI_Finalize();
    return 0;
}
