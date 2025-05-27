from dataclasses import dataclass
from .baseTableModel import BaseTableModel


@dataclass
class MmsRtbmIndicativeDisp(BaseTableModel):
    __tablename__ = "MMS_RTBM_INDICATIVE_DISP"

    id: int
    resourceId: int
    dayTimestamp: str
    indicativeDispSchedule: list[dict[str, str | float | None]]

    def to_db(self):
        return {
            "resourceId": self.resourceId,
            "dayTimestamp": self.dayTimestamp,
            "indicativeDispSchedule": self.indicativeDispSchedule,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            resourceId=data["resourceId"],
            dayTimestamp=data["dayTimestamp"],
            indicativeDispSchedule=data["indicativeDispSchedule"],
        )
