from enum import Enum


class BaseEnum(str, Enum):
    def __get__(self, instance, owner):
        return self.value


class RtbmFlowDirection(BaseEnum):
    UP = "UP"
    DOWN = "DOWN"


class RtbmReserveProcessType(BaseEnum):
    FCR = "FCR"
    aFRR = "aFRR"
    mFRR = "mFRR"

    @classmethod
    def from_process_code(cls, code: str):
        match code:
            case "A47":
                return cls.mFRR
            case "A51":
                return cls.aFRR
            case "A52":
                return cls.FCR

    @classmethod
    def from_business_code(cls, code: str):
        match code:
            case "A95":
                return cls.FCR
            case "A96":
                return cls.aFRR
            case "A97":
                return cls.mFRR
