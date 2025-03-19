from dataclasses import dataclass
import datetime as dt

from .baseTableModel import BaseTableModel


@dataclass
class MmsResourceObjectForecast(BaseTableModel):
    __tablename__ = "MMS_RESOURCE_OBJECT_FORECAST"

    id: int
    resourceId: int
    dayTimestamp: dt.date
    forecast: list[dict[str, str | float | None]]
    totalDayImportEnergy: float
    totalDayExportEnergy: float

    def to_db(self):
        return {
            "id": self.id,
            "resourceId": self.resourceId,
            "dayTimestamp": self.dayTimestamp.strftime("%Y-%m-%d") if self.dayTimestamp else None,
            "forecast": self.forecast,
            "totalDayImportEnergy": round(self.totalDayImportEnergy, 3),
            "totalDayExportEnergy": round(self.totalDayExportEnergy, 3),
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            resourceId=data["resourceId"],
            dayTimestamp=data["dayTimestamp"],
            forecast=data["forecast"],
            totalDayImportEnergy=data["totalDayImportEnergy"],
            totalDayExportEnergy=data["totalDayExportEnergy"],
        )
