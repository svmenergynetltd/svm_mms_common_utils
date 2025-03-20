from dataclasses import dataclass
from .baseTableModel import BaseTableModel


@dataclass
class MmsDamClearingPrices(BaseTableModel):
    __tablename__ = "MMS_DAM_CLEARING_PRICES"

    id: int
    dayTimestamp: str
    clearingPrices: list[dict[str, str | float | None]]

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            dayTimestamp=data["dayTimestamp"],
            clearingPrices=data["clearingPrices"],
        )

    def to_db(self):
        return {
            "dayTimestamp": self.dayTimestamp,
            "clearingPrices": self.clearingPrices,
        }
