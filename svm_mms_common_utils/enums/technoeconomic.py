from enum import Enum


class BaseEnum(str, Enum):
    def __get__(self, instance, owner):
        return self.value


class NonAvailabilityType(str, Enum):
    PARTIAL_Z01 = "Z01"
    TOTAL_Z02 = "Z02"
    CANCEL_Z03 = "Z03"

    @classmethod
    def from_name(cls, name: str):
        for member in cls:
            if member.name == name:
                return member
        return None


class NonAvailabilityReason(BaseEnum):
    B18 = "B18"
    B19 = "B19"
    B20 = "B20"
    A95 = "A95"
    Z01 = "Z01"
    Z02 = "Z02"
    Z03 = "Z03"
    Z04 = "Z04"
    Z05 = "Z05"
    Z06 = "Z06"
