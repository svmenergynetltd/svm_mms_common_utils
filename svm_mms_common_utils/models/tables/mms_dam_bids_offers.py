from dataclasses import dataclass
import datetime as dt
from svm_mms_common_utils.enums import DamBidsOffersTypes
from .baseTableModel import BaseTableModel


@dataclass
class MmsDamBidsOffers(BaseTableModel):
    __tablename__ = "MMS_DAM_BIDS_AND_OFFERS"

    id: int
    resourceId: int
    dayTimestamp: dt.date
    businessType: DamBidsOffersTypes
    totalQuantity: float
    bidsAndOffers: list[dict[str, str | float | None]]
    createdBy: str

    def to_db(self):
        return {
            "id": self.id,
            "resourceId": self.resourceId,
            "dayTimestamp": self.dayTimestamp.strftime("%Y-%m-%d") if self.dayTimestamp else None,
            "businessType": self.businessType,
            "totalQuantity": round(self.totalQuantity, 3),
            "bidsAndOffers": self.bidsAndOffers,
            "createdBy": self.createdBy,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            resourceId=data["resourceId"],
            dayTimestamp=data["dayTimestamp"],
            businessType=DamBidsOffersTypes[data["businessType"]],
            totalQuantity=data["totalQuantity"],
            bidsAndOffers=data["bidsAndOffers"],
            createdBy=data["createdBy"],
        )
