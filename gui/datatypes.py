from enum import Enum


class Datatype(Enum):
    other = 1
    folder = 2
    txt = 3
    png = 4
    jpg = 5
    jpeg = 6
    mp4 = 7
    pdf = 8
    py = 9
    cpp = 10
    hpp = 11



class Bytes(Enum):
    B = 1
    KB = 2
    MB = 3
    GB = 4
    TB = 5
    def __str__(self):
        return f"{self.name}"