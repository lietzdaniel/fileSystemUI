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
    if (argc >= 2)
    {
        auto startTime = std::chrono::high_resolution_clock::now();
        for (int i = 1; i < argc; ++i)
        {
            for (const auto &entry : fs::recursive_directory_iterator(fs::path(argv[i])))
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
        }
        const auto [amount, unit] = convertBytesToString(allBytes);
        auto endTime = std::chrono::high_resolution_clock::now();
        auto totalTime = std::chrono::duration_cast<std::chrono::duration<double>>(endTime - startTime);
        float roundedTime = std::round(totalTime.count()* 10000) / 10000;
        std::cout << "Total size of all folders: " << amount << " " << unit << "in " << fileAmount <<  " files."<< std::endl;
        std::cout << "Finished Benchmarking C++. The calculation took " << roundedTime  << " seconds." << std::endl;
        return 0;
    }
    else
    {
        std::cout << "No folder provided" << std::endl;
        return 1;
    }
}
