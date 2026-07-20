from dataclasses import dataclass
from .baseTableModel import BaseTableModel
from svm_mms_common_utils.enums import RtbmReserveProcessType, RtbmFlowDirection


@dataclass
class MmsRtbmReserveCapacityOffers(BaseTableModel):
    __tablename__ = "MMS_RTBM_RESERVE_CAPACITY_OFFERS"

    id: int
    resourceId: int
    dayTimestamp: str
    processType: RtbmReserveProcessType
    flowDirection: RtbmFlowDirection
    totalQuantity: float
    reserveCapacity: list[dict[str, str | float | None]]
    createdBy: str

    def to_db(self):
        return {
            "id": self.id,
            "resourceId": self.resourceId,
            "dayTimestamp": self.dayTimestamp,
            "processType": self.processType,
            "flowDirection": self.flowDirection,
            "totalQuantity": round(self.totalQuantity, 3),
            "reserveCapacity": self.reserveCapacity,
            "createdBy": self.createdBy,
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
            reserveCapacity=data["reserveCapacity"],
            createdBy=data["createdBy"],
        )
