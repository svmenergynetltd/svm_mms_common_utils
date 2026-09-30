from dataclasses import dataclass

from .base_table_model import BaseTableModel


@dataclass
class MmsDamClearingPrices(BaseTableModel):
    __tablename__ = "MMS_DAM_CLEARING_PRICES"

    dayTimestamp: str
    clearingPrices: list[dict[str, str | float | None]]
    id: int | None = None

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data.get("id"),
            dayTimestamp=data["dayTimestamp"],
            clearingPrices=data["clearingPrices"],
        )

    def to_db(self):
        return {
            "dayTimestamp": self.dayTimestamp,
            "clearingPrices": self.clearingPrices,
        }
