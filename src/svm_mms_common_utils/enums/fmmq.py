from enum import Enum


class BaseEnum(str, Enum):
    def __get__(self, instance, owner):
        return self.value


class FmmqDocStatus(BaseEnum):
    INTERMEDIATE = "INTERMEDIATE"
    FINAL = "FINAL"
    UNKNOWN = "UNKNOWN"
