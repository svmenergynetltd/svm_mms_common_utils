from enum import Enum


class BaseEnum(str, Enum):
    def __get__(self, instance, owner):
        return self.value


class NominationType(BaseEnum):
    OFFTAKE = "OFFTAKE"
    DELIVERY = "DELIVERY"


class RtbmFlowDirection(BaseEnum):
    UP = "UP"
    DOWN = "DOWN"


class ContractStatus(BaseEnum):
    PENDING = "PENDING"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    CONFIRMED = "CONFIRMED"
    ANOMALY_DETECTED = "ANOMALY_DETECTED"
    SELF_CONTRACT = "SELF_CONTRACT"
    SUBMIT_FAILED = "SUBMIT_FAILED"
    MUST_RUN = "MUST_RUN"
