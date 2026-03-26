from dataclasses import dataclass
from .baseTableModel import BaseTableModel


@dataclass
class MmsParticipantFmmq(BaseTableModel):
    __tablename__ = "MMS_PARTICIPANT_FMMQ"

    id: int
    participantId: int
    dayTimestamp: str
    fmmqTimeseries: list[dict[str, str | float | None]]
    totalFMMQ: float
    averageFMMQ: float

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            dayTimestamp=data["dayTimestamp"],
            participantId=data["participantId"],
            fmmqTimeseries=data["fmmqTimeseries"],
            totalFMMQ=data["totalFMMQ"],
            averageFMMQ=data["averageFMMQ"],
        )

    def to_db(self):
        return {
            "dayTimestamp": self.dayTimestamp,
            "participantId": self.participantId,
            "fmmqTimeseries": self.fmmqTimeseries,
            "totalFMMQ": round(self.totalFMMQ, 3),
            "averageFMMQ": round(self.averageFMMQ, 3),
        }
