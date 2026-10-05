from dataclasses import dataclass

from svm_mms_common_utils.enums import RtbmFlowDirection, RtbmReserveProcessType

from .base_table_model import BaseTableModel


@dataclass
class MmsRtbmReserveCapacityOffers(BaseTableModel):
    __tablename__ = "MMS_RTBM_RESERVE_CAPACITY_OFFERS"

    id: int | None
    resourceId: int
    dayTimestamp: str
    processType: RtbmReserveProcessType
    flowDirection: RtbmFlowDirection
    totalQuantity: float
    quantities: list[dict[str, str | float | None]]
    pricingStrategy: dict[str, str | float | None]
    createdBy: str
    pricesCreatedBy: str

    def to_db(self):
        return {
            "resourceId": self.resourceId,
            "dayTimestamp": self.dayTimestamp,
            "processType": self.processType,
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
            dayTimestamp=data["dayTimestamp"],
            processType=RtbmReserveProcessType[data["processType"]],
            flowDirection=RtbmFlowDirection[data["flowDirection"]],
            totalQuantity=data["totalQuantity"],
            quantities=data["quantities"],
            pricingStrategy=data["pricingStrategy"],
            createdBy=data["createdBy"],
            pricesCreatedBy=data["pricesCreatedBy"],
        )
