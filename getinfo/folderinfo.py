import os
from datatypes import Datatype
from typing import Iterator,Tuple
def returnItems(folderPath: str) -> Iterator[Tuple[str,Datatype]]:
    """Returns an iterator for all items in a folder

    Args:
        folderPath (str): Path to folder

    Return:
        Generator[Tuple[str,Datatype]]: Generator of the items in the folder
    """
    for file in os.listdir(folderPath):
        file = os.path.join(folderPath,file)
        if os.path.isfile(file):
            _, file_extension = os.path.splitext(file)
            file_extension.upper()
            file_extension = file_extension[1:]
            try: 
              
                yield (file,Datatype[file_extension])
            except:
                yield (file,Datatype.other)
        else:
            yield (file,Datatype.folder)
   
    
def returnFolderSize(folderPath: str) -> int:
    
    byteCtr = 0
    for file in os.listdir(folderPath):
        file = os.path.join(folderPath,file)
        if os.path.isfile(file):
            byteCtr += os.path.getsize(file)
        else:
            byteCtr += returnFolderSize(file)
        
    return byteCtr


