from enum import Enum


class BaseEnum(str, Enum):
    def __get__(self, instance, owner):
        return self.value


class DamBidsOffersTypes(BaseEnum):
    SIMPLE_BIDS = "SIMPLE_BIDS"
    SIMPLE_OFFER = "SIMPLE_OFFER"
    BLOCK_OFFER = "BLOCK_OFFER"


class DamPricingStrategyTypes(BaseEnum):
    FIXED_PRICE = "fixedPrice"
    VARIABLE_PRICE = "variablePrice"
    STEP_OFFERS = "stepOffers"
    BLOCK_OFFERS = "blockOffers"
