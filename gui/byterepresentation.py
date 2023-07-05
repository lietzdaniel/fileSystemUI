from .datatypes import Bytes

class ByteRepresentation:
    def __init__(self, amount:float, unit: Bytes = None):
        if type(amount) == str:
            splitted = amount.split(" ")
            self.amount = float(splitted[0])
            self.unit = Bytes[splitted[1]]
        else:
            self.amount = amount
            self.unit = unit
    
    def __gt__(self, other):
        if isinstance(other, ByteRepresentation):
            return self.amount * (1000**self.unit.value) > other.amount * (1000**other.unit.value)
        return NotImplemented
    def __lt__(self, other):
        
        if isinstance(other, ByteRepresentation):
            return self.amount * (1000**self.unit.value) < other.amount * (1000**other.unit.value)
        return NotImplemented
    def __str__(self):
        return f"{self.amount} {self.unit}"
