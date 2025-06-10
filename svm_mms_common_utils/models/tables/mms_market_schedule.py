from dataclasses import dataclass
from .baseTableModel import BaseTableModel


@dataclass
class MmsMarketSchedule(BaseTableModel):
    __tablename__ = "MMS_MARKET_SCHEDULE"

    id: int
    resourceId: int
    dayTimestamp: str
    totalScheduledEnergy: float
    marketSchedule: list[dict[str, str | float | None]]

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            resourceId=data["resourceId"],
            dayTimestamp=data["dayTimestamp"],
            totalScheduledEnergy=data["totalScheduledEnergy"],
            marketSchedule=data["marketSchedule"],
        )

    def to_db(self):
        return {
            "resourceId": self.resourceId,
            "dayTimestamp": self.dayTimestamp,
            "totalScheduledEnergy": round(self.totalScheduledEnergy, 3),
            "marketSchedule": self.marketSchedule,
        }
