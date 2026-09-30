from dataclasses import dataclass

from .base_table_model import BaseTableModel


@dataclass
class MmsDamFcastedClearingPrices(BaseTableModel):
    __tablename__ = "MMS_DAM_FORECASTED_CLEARING_PRICES"

    dayTimestamp: str
    forecastedClearingPrices: list[dict[str, str | float | None]]
    id: int | None = None

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data.get("id"),
            dayTimestamp=data["dayTimestamp"],
            forecastedClearingPrices=data["forecastedClearingPrices"],
        )

    def to_db(self):
        return {
            "dayTimestamp": self.dayTimestamp,
            "forecastedClearingPrices": self.forecastedClearingPrices,
        }
