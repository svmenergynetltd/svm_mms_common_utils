from dataclasses import dataclass
from .baseTableModel import BaseTableModel
from svm_mms_common_utils.enums import FmmqDocStatus


@dataclass
class MmsParticipantFmmq(BaseTableModel):
    __tablename__ = "MMS_PARTICIPANT_FMMQ"

    id: int
    participantId: int
    dayTimestamp: str
    documentStatus: FmmqDocStatus
    fmmqTimeseries: list[dict[str, str | float | None]]
    totalFMMQ: float
    averageFMMQ: float
    xmlFile: str | None = None

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            participantId=data["participantId"],
            dayTimestamp=data["dayTimestamp"],
            documentStatus=FmmqDocStatus[data["documentStatus"]],
            fmmqTimeseries=data["fmmqTimeseries"],
            totalFMMQ=data["totalFMMQ"],
            averageFMMQ=data["averageFMMQ"],
            xmlFile=data.get("xmlFile"),
        )

    def to_db(self):
        return {
            "participantId": self.participantId,
            "dayTimestamp": self.dayTimestamp,
            "documentStatus": self.documentStatus,
            "fmmqTimeseries": self.fmmqTimeseries,
            "totalFMMQ": round(self.totalFMMQ, 3),
            "averageFMMQ": round(self.averageFMMQ, 3),
            "xmlFile": self.xmlFile,
        }
