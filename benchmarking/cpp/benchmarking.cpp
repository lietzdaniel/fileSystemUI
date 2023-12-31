#include "benchmarking.hpp"
#include <iostream>
#include <string>
#include <fstream>
#include <filesystem>
#include <chrono>
#include <cmath>

std::tuple<float, std::string> convertBytesToString(const std::vector<int> &allBytes)
{
    std::vector<std::string> units{"bytes", "kilobytes", "megabytes", "gigabytes", "terabytes"};
    float amount = 0.0;
    std::string unit = "";

    for (int i = units.size() - 1; i >= 0; i--)
    {

        if (allBytes[i] == 0)
            continue;
        if (amount == 0.0)
        {
            amount += static_cast<float>(allBytes[i]);
            unit = units[i];
            continue;
        }
        amount += static_cast<float>(allBytes[i]) / 1000.0;
        break;
    }

    return std::make_tuple(amount, unit);
}

int main(int argc, char *argv[])
{
    // 'bytes', 'kilobytes', 'megabytes', 'gigabytes', 'terabytes'
    std::vector<int> allBytes{0, 0, 0, 0, 0};
    int fileAmount = 0;
    fs::path benchMarkFolder;
    if (argc >= 2)
    {
        benchMarkFolder = fs::path(argv[1]);
    }
    else
    {
        std::cout << "Using ./benchmarking/benchmarkfolders as Benchmark" << std::endl;
        benchMarkFolder = fs::path("./benchmarking/benchmarkfolders");
    }

    for (const auto &entry : fs::recursive_directory_iterator(fs::path(benchMarkFolder)))
    {
        if (fs::is_regular_file(entry))
        {
            fileAmount++;
            allBytes[0] += fs::file_size(entry);
            int idx = 0;

            while (idx < allBytes.size() - 1)
            {

                while (allBytes[idx] > 1000)
                {
                    long transferredBytes = allBytes[idx] / 1000;
                    allBytes[idx + 1] += transferredBytes;
                    allBytes[idx] -= transferredBytes * 1000;
                }
                idx++;
            }
        }
    }

    const auto [amount, unit] = convertBytesToString(allBytes);

    std::cout << "Total size of all folders: " << amount << " " << unit << " in " << fileAmount << " files." << std::endl;
    return 0;
}
