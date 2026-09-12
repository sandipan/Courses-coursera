#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <mpi.h>

int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Seed random number generator
    srand(time(nullptr) + rank);

    // Generate a random number
    int my_number = rand() % 100;
    std::cout << "Process " << rank << " generated: " << my_number << std::endl;

    int received_number;
    int left_neighbor = (rank - 1 + size) % size;
    int right_neighbor = (rank + 1) % size;

    MPI_Request send_request, recv_request;

    // TODO: Implement non-blocking send to right neighbor using MPI_Isend
    MPI_Isend(&my_number, 1, MPI_INT, right_neighbor, rank, MPI_COMM_WORLD, &send_request);

    // TODO: Implement non-blocking receive from left neighbor using MPI_Irecv
    MPI_Irecv(&received_number, 1, MPI_INT, left_neighbor, left_neighbor, MPI_COMM_WORLD, &recv_request);

    // TODO: Wait for both send and receive to complete using MPI_Wait
    MPI_Wait(&send_request, MPI_STATUS_IGNORE);
    MPI_Wait(&recv_request, MPI_STATUS_IGNORE);

    int sum = my_number + received_number;
    std::cout << "Process " << rank << " sum: " << sum << std::endl;

    // Gather results at root process
    std::vector<int> all_sums;
    if (rank == 0)
    {
        all_sums.resize(size);
    }

    MPI_Gather(&sum, 1, MPI_INT, all_sums.data(), 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank == 0)
    {
        std::cout << "All sums:" << std::endl;
        for (int i = 0; i < size; ++i)
        {
            std::cout << "Process " << i << ": " << all_sums[i] << std::endl;
        }
    }

    MPI_Finalize();
    return 0;
}

// Compile and Run
// mpic++ -o ring_communication ring_communication.cpp
// mpirun -np 4 ./ring_communication