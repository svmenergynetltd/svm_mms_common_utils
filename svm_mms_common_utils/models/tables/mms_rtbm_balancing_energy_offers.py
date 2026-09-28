from dataclasses import dataclass
from .baseTableModel import BaseTableModel
from svm_mms_common_utils.enums import RtbmFlowDirection


@dataclass
class MmsRtbmBalancingEnergyOffers(BaseTableModel):
    __tablename__ = "MMS_RTBM_BALANCING_ENERGY_OFFERS"

    id: int
    resourceId: int
    dayTimestamp: str
    flowDirection: RtbmFlowDirection
    totalQuantity: float
    quantities: list[dict[str, str | float | None]]
    pricingStrategy: dict[str, str | float | None]
    createdBy: str
    pricesCreatedBy: str

    def to_db(self):
        return {
            "resourceId": self.resourceId,
            "dayTimestamp": self.dayTimestamp.strftime("%Y-%m-%d")
            if self.dayTimestamp
            else None,
            "flowDirection": self.flowDirection,
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
            flowDirection=RtbmFlowDirection[data["flowDirection"]],
            dayTimestamp=data["dayTimestamp"],
            totalQuantity=data["totalQuantity"],
            quantities=data["quantities"],
            pricingStrategy=data["pricingStrategy"],
            createdBy=data["createdBy"],
            pricesCreatedBy=data["pricesCreatedBy"],
        )
