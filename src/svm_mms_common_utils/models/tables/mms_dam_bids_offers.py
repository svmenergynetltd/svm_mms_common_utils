import datetime as dt
from dataclasses import dataclass

from svm_mms_common_utils.enums import DamBidsOffersTypes

from .base_table_model import BaseTableModel


@dataclass
class MmsDamBidsOffers(BaseTableModel):
    __tablename__ = "MMS_DAM_BIDS_AND_OFFERS"

    id: int | None
    resourceId: int
    dayTimestamp: dt.date
    businessType: DamBidsOffersTypes
    totalQuantity: float
    quantities: list[dict[str, str | float | None]]
    pricingStrategy: dict[str, str | float | None]
    createdBy: str
    pricesCreatedBy: str

    def to_db(self):
        return {
            "resourceId": self.resourceId,
            "dayTimestamp": self.dayTimestamp.strftime("%Y-%m-%d") if self.dayTimestamp else None,
            "businessType": self.businessType,
            "totalQuantity": round(self.totalQuantity, 3),
            "quantities": self.quantities,
            "pricingStrategy": self.pricingStrategy,
            "createdBy": self.createdBy,
            "pricesCreatedBy": self.pricesCreatedBy,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            resourceId=data["resourceId"],
            dayTimestamp=data["dayTimestamp"],
            businessType=DamBidsOffersTypes[data["businessType"]],
            totalQuantity=data["totalQuantity"],
            quantities=data["quantities"],
            pricingStrategy=data["pricingStrategy"],
            createdBy=data["createdBy"],
            pricesCreatedBy=data["pricesCreatedBy"],
        )
