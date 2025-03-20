from dataclasses import dataclass
from .baseTableModel import BaseTableModel


@dataclass
class MmsDamExpectedLoadMargin(BaseTableModel):
    __tablename__ = "MMS_DAM_EXPECTED_LOAD_MARGIN"

    id: int
    resourceId: int
    dayTimestamp: str
    totalMargin: float
    damMargin: list[dict[str, str | float | None]]

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            dayTimestamp=data["dayTimestamp"],
            resourceId=data["resourceId"],
            totalMargin=data["totalMargin"],
            damMargin=data["damMargin"],
        )

    def to_db(self):
        return {
            "dayTimestamp": self.dayTimestamp,
            "resourceId": self.resourceId,
            "totalMargin": round(self.totalMargin, 3),
            "damMargin": self.damMargin,
        }
