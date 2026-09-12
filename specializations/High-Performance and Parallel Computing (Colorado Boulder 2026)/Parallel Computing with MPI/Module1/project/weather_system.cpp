#include <iostream>
#include <mpi.h>
#include <string>

struct WeatherData
{
    int station_id;
    double temperature;
    double humidity;
};

std::string predict_weather(double avg_temp, double avg_humidity)
{
    if (avg_temp > 30 && avg_humidity > 70)
        return "Hot and Humid";
    if (avg_temp > 30)
        return "Hot";
    if (avg_temp < 10)
        return "Cold";
    if (avg_humidity > 80)
        return "Rainy";
    return "Pleasant";
}

int main(int argc, char **argv)
{
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size < 4)
    {
        std::cerr << "This program requires at least 4 processes." << std::endl;
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    if (rank == 0)
    { // Central Coordinator
        WeatherData data;
        double total_temp = 0, total_humidity = 0;
        int stations = size - 1;

        for (int i = 1; i <= stations; i++)
        {
            // TODO: Implement MPI_Recv to receive WeatherData from station i
            // Use MPI_ANY_TAG for the tag parameter
            MPI_Recv(&data, sizeof(WeatherData),
                     MPI_BYTE, i, MPI_ANY_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

            std::cout << "Received from station " << data.station_id
                      << ": Temp = " << data.temperature
                      << "°C, Humidity = " << data.humidity << "%" << std::endl;

            total_temp += data.temperature;
            total_humidity += data.humidity;
        }

        double avg_temp = total_temp / stations;
        double avg_humidity = total_humidity / stations;

        std::cout << "\nAverage Temperature: " << avg_temp << "°C" << std::endl;
        std::cout << "Average Humidity: " << avg_humidity << "%" << std::endl;
        std::cout << "Weather Prediction: " << predict_weather(avg_temp, avg_humidity) << std::endl;
    }
    else
    { // Weather Stations
        WeatherData data;
        data.station_id = rank;

        // Constant values for each station
        if (rank == 1)
        {
            data.temperature = 25.0;
            data.humidity = 60.0;
        }
        else if (rank == 2)
        {
            data.temperature = 32.0;
            data.humidity = 75.0;
        }
        else
        {
            data.temperature = 18.0;
            data.humidity = 85.0;
        }

        // TODO: Implement MPI_Send to send WeatherData to the central coordinator (rank 0)
        // Use 0 for the tag parameter
        MPI_Send(&data, sizeof(WeatherData),
                 MPI_BYTE, 0, 0, MPI_COMM_WORLD);

        std::cout << "Station " << rank << " sent data: Temp = " << data.temperature
                  << "°C, Humidity = " << data.humidity << "%" << std::endl;
    }

    MPI_Finalize();
    return 0;
}
