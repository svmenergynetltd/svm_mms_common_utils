from enum import Enum


class NominationType(str, Enum):
    OFFTAKE = "OFFTAKE"
    DELIVERY = "DELIVERY"


class DamBidsOffersTypes(str, Enum):
    SIMPLE_BIDS = "SIMPLE_BIDS"
    SIMPLE_OFFER = "SIMPLE_OFFER"
    BLOCK_OFFER = "BLOCK_OFFER"
