from dataclasses import dataclass
import datetime as dt

from .baseTableModel import BaseTableModel
from svm_mms_common_utils.enums import SettlDocStatus


@dataclass
class MmsSettlements(BaseTableModel):
    __tablename__ = "MMS_SETTLEMENTS"

    id: int
    dayTimestamp: dt.date
    participantId: int
    resourceId: int
    documentMRID: str
    timeseriesMRID: str
    documentStatus: SettlDocStatus
    resolution: str
    statementType: str
    businessType: str
    data: list[dict[str, str | float | None]]

    def to_db(self):
        return {
            "id": self.id,
            "dayTimestamp": self.dayTimestamp.strftime("%Y-%m-%d"),
            "participantId": self.participantId,
            "resourceId": self.resourceId,
            "documentMRID": self.documentMRID,
            "timeseriesMRID": self.timeseriesMRID,
            "documentStatus": self.documentStatus,
            "resolution": self.resolution,
            "statementType": self.statementType,
            "businessType": self.businessType,
            "data": self.data,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            dayTimestamp=data["dayTimestamp"],
            participantId=data["participantId"],
            resourceId=data["resourceId"],
            documentMRID=data["documentMRID"],
            timeseriesMRID=data["timeseriesMRID"],
            documentStatus=SettlDocStatus[data["documentStatus"]],
            resolution=data["resolution"],
            statementType=data["statementType"],
            businessType=data["businessType"],
            data=data["data"],
        )
