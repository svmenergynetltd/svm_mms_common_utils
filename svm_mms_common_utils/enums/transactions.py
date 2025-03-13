from enum import Enum


class BaseEnum(str, Enum):
    def __get__(self, instance, owner):
        return self.value


class TransactionStatus(BaseEnum):
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"


class TrxSubmissionType(BaseEnum):
    FETCH_MARKET_SCHEDULE = "FETCH_MARKET_SCHEDULE"
    FETCH_CLEARING_PRICES = "FETCH_CLEARING_PRICES"
    FETCH_FCAST_CLEARING_PRICES = "FETCH_FCAST_CLEARING_PRICES"
    FETCH_DAM_MARGIN = "FETCH_DAM_MARGIN"
    FETCH_DAM_CLEARED_ENERGY = "FETCH_DAM_CLEARED_ENERGY"

    FM_CONTRACT = "FM_CONTRACT"
    FM_NOMINATION = "FM_NOMINATION"
    DAM_BIDS = "DAM_BIDS"
    DAM_OFFERS = "DAM_OFFERS"
