from dataclasses import dataclass
import datetime as dt

from .baseTableModel import BaseTableModel
from svm_mms_common_utils.enums import NominationType


@dataclass
class MmsPhysicalNomination(BaseTableModel):
    __tablename__ = "MMS_PHYSICAL_NOMINATIONS"

    id: int
    dayTimestamp: dt.date
    resourceId: int
    nomination: list[dict[str, str | float | None]]
    totalDayEnergy: float
    energyFlow: NominationType
    createdBy: str

    def to_db(self):
        return {
            "id": self.id,
            "dayTimestamp": self.dayTimestamp.strftime("%Y-%m-%d") if self.dayTimestamp else None,
            "resourceId": self.resourceId,
            "nomination": self.nomination,
            "totalDayEnergy": round(self.totalDayEnergy, 3),
            "energyFlow": self.energyFlow,
            "createdBy": self.createdBy,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            dayTimestamp=data["dayTimestamp"],
            resourceId=data["resourceId"],
            nomination=data["nomination"],
            totalDayEnergy=data["totalDayEnergy"],
            energyFlow=NominationType[data["energyFlow"]],
            createdBy=data["createdBy"],
        )
