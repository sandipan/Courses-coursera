#include <iostream>
#include <mpi.h>

struct Point3D {
    double x;
    double y;
    double z;
};

void create_mpi_point3d_type(MPI_Datatype* mpi_point3d_type) {
    int block_lengths[3] = {1, 1, 1};
    MPI_Aint displacements[3];
    MPI_Datatype types[3] = {MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE};

    displacements[0] = offsetof(Point3D, x);
    displacements[1] = offsetof(Point3D, y);
    displacements[2] = offsetof(Point3D, z);

    // TODO: Create the derived data type
    // Use MPI_Type_create_struct to create the MPI datatype
    MPI_Type_create_struct(3, block_lengths, displacements, types, mpi_point3d_type);
    // TODO: Commit the new type using MPI_Type_commit
    MPI_Type_commit(mpi_point3d_type);
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    MPI_Datatype mpi_point3d_type;
    create_mpi_point3d_type(&mpi_point3d_type);

    if (rank == 0) {
        Point3D point = {1.0, 2.0, 3.0};
        std::cout << "Process 0 sending point: (" << point.x << ", " << point.y << ", " << point.z << ")" << std::endl;

        // TODO: Send the Point3D structure using MPI_Send
        MPI_Send(&point, 1, mpi_point3d_type, 1, rank, MPI_COMM_WORLD);
    }
    else if (rank == 1)
    {
        Point3D point;
        
        // TODO: Receive the Point3D structure using MPI_Recv
        MPI_Recv(&point, 1, mpi_point3d_type, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        std::cout << "Process 1 received point: (" << point.x << ", " << point.y << ", " << point.z << ")" << std::endl;
    }

    MPI_Type_free(&mpi_point3d_type);
    MPI_Finalize();
    return 0;
}

// mpic++ -o mpi_derived_type mpi_derived_type.cpp
// mpirun -np 2 ./mpi_derived_type