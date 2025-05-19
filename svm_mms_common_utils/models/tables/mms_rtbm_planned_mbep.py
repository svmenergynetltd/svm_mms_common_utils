from dataclasses import dataclass
from .baseTableModel import BaseTableModel


@dataclass
class MmsRtbmPlannedMbep(BaseTableModel):
    __tablename__ = "MMS_RTBM_PLANNED_MBEP"

    id: int
    dayTimestamp: str
    pricesPlannedMbep: list[dict[str, str | float | None]]

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            dayTimestamp=data["dayTimestamp"],
            pricesPlannedMbep=data["pricesPlannedMbep"],
        )

    def to_db(self):
        return {
            "dayTimestamp": self.dayTimestamp,
            "pricesPlannedMbep": self.pricesPlannedMbep,
        }
