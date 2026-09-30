from dataclasses import dataclass

from .base_table_model import BaseTableModel


@dataclass
class MmsRtbmMbep(BaseTableModel):
    __tablename__ = "MMS_RTBM_MBEP"

    dayTimestamp: str
    pricesMbep: list[dict[str, str | float | None]]
    id: int | None = None

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data.get("id"),
            dayTimestamp=data["dayTimestamp"],
            pricesMbep=data["pricesMbep"],
        )

    def to_db(self):
        return {
            "dayTimestamp": self.dayTimestamp,
            "pricesMbep": self.pricesMbep,
        }
