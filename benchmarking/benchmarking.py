import os
import time
import logging
import subprocess
from typing import List, Tuple

logging.basicConfig(level=logging.INFO)


def convertBytesToString(allBytes: List[int]) -> Tuple[float, str]:
    """Convert Bytes to most optimal Unit

    Args:
        allBytes (List[int]): List of bytes with units bytes to terabytes

    Return:
        float: Amount of the optimal unit.
        str: Optimal unit.
    """
    units = ["bytes", "kilobytes", "megabytes", "gigabytes", "terabytes"]
    amount = 0.0
    unit = ""
    for i in reversed(range(0, len(units))):
        if allBytes[i] == 0:
            continue
        if amount == 0.0:
            amount += allBytes[i]
            unit = units[i]
            continue
        amount += allBytes[i] / 1000
        break
    return amount, unit


if __name__ == "__main__":
    logging.info(
        "Benchmarking C++ and Python file reading speed on all folders in benchmarking."
    )
    
    benchMarkFolder = "./benchmarking/benchmarkfolders"
    cppPath = "./benchmarking/cppBenchmark"
    # 'bytes', 'kilobytes', 'megabytes', 'gigabytes', 'terabytes'
    allBytes = [0, 0, 0, 0, 0]
    fileAmount = 0
    logging.info("Benchmarking Python...")
    # Python folder size calculation
    
    folderSizeBytes = 0
    pythonStartTime = time.time()
    for root, dirs, files in os.walk(benchMarkFolder):
        for file in files:
            fileAmount += 1
            curFile = os.path.join(root, file)
            allBytes[0] += os.path.getsize(curFile)
            idx = 0
            while idx < len(allBytes) - 1:
                while allBytes[idx] > 1000:
                    transferredBytes = allBytes[idx] // 1000
                    allBytes[idx + 1] += transferredBytes
                    allBytes[idx] -= transferredBytes * 1000
                idx += 1
    amount, unit = convertBytesToString(allBytes)
    pythonEndTime = time.time()
    pythonTotalTime = pythonEndTime - pythonStartTime
    logging.info(f"Total size of all folders: {amount} {unit} in {fileAmount} files.")
    logging.info(f"Finished Benchmarking Python. The calculation took {round(pythonTotalTime,4)} seconds.")

