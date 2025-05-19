from dataclasses import dataclass
from .baseTableModel import BaseTableModel


@dataclass
class MmsRtbmMbep(BaseTableModel):
    __tablename__ = "MMS_RTBM_MBEP"

    id: int
    dayTimestamp: str
    pricesMbep: list[dict[str, str | float | None]]

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            dayTimestamp=data["dayTimestamp"],
            pricesMbep=data["pricesMbep"],
        )

    def to_db(self):
        return {
            "dayTimestamp": self.dayTimestamp,
            "pricesMbep": self.pricesMbep,
        }
