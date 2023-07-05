import os
from .datatypes import Datatype, Bytes
from typing import Iterator, Tuple
from .byterepresentation import ByteRepresentation
import time









def returnItems(folderPath: str) -> Iterator[Tuple[str, Datatype]]:
    """Returns an iterator for all items in a folder

    Args:
        folderPath (str): Path to folder

    Return:
        Generator[Tuple[str,str,float,Datatype]]: Generator of the items in the folder (name,size,last modified time, datatype)
    """
    for file in os.listdir(folderPath):
        oldFile = file
        file = os.path.join(folderPath, file)
        if os.path.isfile(file):
            _, fileExtension = os.path.splitext(file)
            fileExtension.upper()
            fileExtension = fileExtension[1:]
            fileSize = convertBytes((int)(os.stat(file).st_size))
            fileDate = convertDatetoString(os.path.getmtime(file))
            try:
                yield (oldFile, fileSize, fileDate, Datatype[fileExtension])
            except:
                yield (oldFile, fileSize, fileDate, Datatype.other)
        else:
            yield (oldFile, convertBytes(returnFolderSize(file)), -1, Datatype.folder)


def returnFolderSize(folderPath: str) -> int:
    byteCtr = 0
    for file in os.listdir(folderPath):
        file = os.path.join(folderPath, file)
        if os.path.isfile(file):
            byteCtr += os.path.getsize(file)
        else:
            byteCtr += returnFolderSize(file)

    return byteCtr


def convertBytes(bytes: int) -> Tuple[float, Bytes]:
    units = ["B", "KB", "MB", "GB", "TB"]
    amount = 0.0
    unit = ""
    idx = 0
    while bytes > 1000 and idx < len(units):
        bytes /= 1000
        idx += 1
    bytes = round(bytes,2)
    
    return ByteRepresentation(bytes,Bytes[units[idx]])


def convertDatetoString(date: float) -> str:
    return time.strftime("%d/%m/%Y", time.localtime(date))
