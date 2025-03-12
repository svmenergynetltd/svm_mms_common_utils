from dataclasses import dataclass
import datetime as dt
from svm_mms_common_utils.enums import DamBidsOffersTypes


@dataclass
class MmsDamBidsOffers:
    id: int
    resourceId: int
    dayTimestamp: dt.date
    businessType: DamBidsOffersTypes
    totalQuantity: float
    bidsAndOffers: str
    createdBy: str

    def to_db(self):
        return {
            "id": self.id,
            "resourceId": self.resourceId,
            "dayTimestamp": self.dayTimestamp.strftime("%Y-%m-%d"),
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
            dayTimestamp=dt.datetime.strptime(data["dayTimestamp"], "%Y-%m-%d").date(),
            businessType=DamBidsOffersTypes[data["businessType"]],
            totalQuantity=data["totalQuantity"],
            bidsAndOffers=data["bidsAndOffers"],
            createdBy=data["createdBy"],
        )
