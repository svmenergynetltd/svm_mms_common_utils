from dataclasses import dataclass
from .baseTableModel import BaseTableModel
from svm_mms_common_utils.enums import RtbmFlowDirection


@dataclass
class MmsRtbmPlannedBEOActivations(BaseTableModel):
    __tablename__ = "MMS_RTBM_PLANNED_BEO_ACTIVATION"

    id: int
    resourceId: int
    dayTimestamp: str
    flowDirection: RtbmFlowDirection
    totalQuantity: float
    balancingEnergy: list[dict[str, str | float | None]]

    def to_db(self):
        return {
            "resourceId": self.resourceId,
            "dayTimestamp": self.dayTimestamp,
            "flowDirection": self.flowDirection,
            "totalQuantity": round(self.totalQuantity, 3),
            "balancingEnergy": self.balancingEnergy,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            resourceId=data["resourceId"],
            flowDirection=RtbmFlowDirection[data["flowDirection"]],
            dayTimestamp=data["dayTimestamp"],
            totalQuantity=data["totalQuantity"],
            balancingEnergy=data["balancingEnergy"],
        )
