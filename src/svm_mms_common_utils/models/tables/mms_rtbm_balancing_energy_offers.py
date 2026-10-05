import datetime as dt
from dataclasses import dataclass

from svm_mms_common_utils.enums import RtbmFlowDirection
from svm_mms_common_utils.utils.dates import DateUtils

from .base_table_model import BaseTableModel


@dataclass
class MmsRtbmBalancingEnergyOffers(BaseTableModel):
    __tablename__ = "MMS_RTBM_BALANCING_ENERGY_OFFERS"

    id: int | None
    resourceId: int
    dayTimestamp: str | dt.date
    flowDirection: RtbmFlowDirection
    totalQuantity: float
    quantities: list[dict[str, str | float | None]]
    pricingStrategy: dict[str, str | float | None]
    createdBy: str
    pricesCreatedBy: str

    def to_db(self):
        return {
            "resourceId": self.resourceId,
            "dayTimestamp": DateUtils.get_date_to_db(self.dayTimestamp),
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
