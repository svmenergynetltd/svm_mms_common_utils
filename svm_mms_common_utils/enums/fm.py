from enum import Enum


class BaseEnum(str, Enum):
    def __get__(self, instance, owner):
        return self.value


class NominationType(BaseEnum):
    OFFTAKE = "OFFTAKE"
    DELIVERY = "DELIVERY"


class DamBidsOffersTypes(BaseEnum):
    SIMPLE_BIDS = "SIMPLE_BIDS"
    SIMPLE_OFFER = "SIMPLE_OFFER"
    BLOCK_OFFER = "BLOCK_OFFER"


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
