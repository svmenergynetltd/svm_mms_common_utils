from enum import Enum


class NominationType(str, Enum):
    OFFTAKE = "OFFTAKE"
    DELIVERY = "DELIVERY"


class DamBidsOffersTypes(str, Enum):
    SIMPLE_BIDS = "SIMPLE_BIDS"
    SIMPLE_OFFER = "SIMPLE_OFFER"
    BLOCK_OFFER = "BLOCK_OFFER"


class ContractStatus(str, Enum):
    PENDING = "PENDING"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    CONFIRMED = "CONFIRMED"
    ANOMALY_DETECTED = "ANOMALY_DETECTED"
    SELF_CONTRACT = "SELF_CONTRACT"
    SUBMIT_FAILED = "SUBMIT_FAILED"
