from dataclasses import dataclass

from .base_table_model import BaseTableModel


@dataclass
class MmsDamClearedEnergy(BaseTableModel):
    __tablename__ = "MMS_DAM_CLEARED_ENERGY"

    resourceId: int
    dayTimestamp: str
    clearedEnergy: list[dict[str, str | float | None]]
    totalBoughtEnergy: float
    totalSoldEnergy: float
    id: int | None = None

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data.get("id"),
            resourceId=data["resourceId"],
            dayTimestamp=data["dayTimestamp"],
            clearedEnergy=data["clearedEnergy"],
            totalBoughtEnergy=data["totalBoughtEnergy"],
            totalSoldEnergy=data["totalSoldEnergy"],
        )

    def to_db(self):
        return {
            "resourceId": self.resourceId,
            "dayTimestamp": self.dayTimestamp,
            "clearedEnergy": self.clearedEnergy,
            "totalBoughtEnergy": round(self.totalBoughtEnergy, 3),
            "totalSoldEnergy": round(self.totalSoldEnergy, 3),
        }
