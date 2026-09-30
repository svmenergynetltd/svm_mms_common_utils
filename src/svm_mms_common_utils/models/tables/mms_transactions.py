import datetime as dt
from dataclasses import dataclass

from ...enums import TransactionStatus, TrxSubmissionType
from .base_table_model import BaseTableModel


@dataclass
class MmsTransactions(BaseTableModel):
    __tablename__ = "MMS_TRANSACTIONS"

    id: int
    submissionType: TrxSubmissionType
    participantId: int
    resourceObjectId: int
    marketDay: dt.date
    scheduledDateTime: dt.datetime
    status: TransactionStatus
    mRID: str | None = None
    revision: int = 1
    databaseRowId: int | None = None
    databaseTableName: str | None = None
    xmlFile: str | None = None
    sentXml: str | None = None
    receivedXml: str | None = None
    dateSent: dt.datetime | None = None
    dateReceived: dt.datetime | None = None
    timeSeries: list[dict] | None = None
    dateAdded: str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dateUpdated: dt.datetime | None = None

    def to_db(self):
        return {
            "mRID": self.mRID,
            "revision": self.revision,
            "status": self.status,
            "submissionType": self.submissionType,
            "scheduledDateTime": (
                self.scheduledDateTime.strftime("%Y-%m-%d %H:%M:%S")
                if self.scheduledDateTime
                else None
            ),
            "databaseRowId": self.databaseRowId,
            "databaseTableName": self.databaseTableName,
            "marketDay": self.marketDay.strftime("%Y-%m-%d") if self.marketDay else None,
            "xmlFile": self.xmlFile,
            "sentXml": self.sentXml,
            "receivedXml": self.receivedXml,
            "dateAdded": self.dateAdded,
            "dateSent": self.dateSent.strftime("%Y-%m-%d %H:%M:%S") if self.dateSent else None,
            "dateReceived": (
                self.dateReceived.strftime("%Y-%m-%d %H:%M:%S") if self.dateReceived else None
            ),
            "participantId": self.participantId,
            "resourceObjectId": self.resourceObjectId,
            "timeSeries": self.timeSeries,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            mRID=data["mRID"],
            revision=data["revision"],
            status=TransactionStatus[data["status"]],
            submissionType=TrxSubmissionType[data["submissionType"]],
            scheduledDateTime=data["scheduledDateTime"],
            databaseRowId=data["databaseRowId"],
            databaseTableName=data["databaseTableName"],
            marketDay=data["marketDay"],
            xmlFile=data["xmlFile"],
            sentXml=data["sentXml"],
            receivedXml=data["receivedXml"],
            dateSent=data["dateSent"],
            dateReceived=data["dateReceived"],
            participantId=data["participantId"],
            resourceObjectId=data["resourceObjectId"],
            timeSeries=data["timeSeries"],
            dateAdded=data["dateAdded"],
            dateUpdated=data["dateUpdated"],
        )
