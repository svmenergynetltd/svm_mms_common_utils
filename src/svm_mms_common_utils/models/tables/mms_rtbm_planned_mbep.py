from dataclasses import dataclass

from .base_table_model import BaseTableModel


@dataclass
class MmsRtbmPlannedMbep(BaseTableModel):
    __tablename__ = "MMS_RTBM_PLANNED_MBEP"

    dayTimestamp: str
    pricesPlannedMbep: list[dict[str, str | float | None]]
    id: int | None = None

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data.get("id"),
            dayTimestamp=data["dayTimestamp"],
            pricesPlannedMbep=data["pricesPlannedMbep"],
        )

    def to_db(self):
        return {
            "dayTimestamp": self.dayTimestamp,
            "pricesPlannedMbep": self.pricesPlannedMbep,
        }
