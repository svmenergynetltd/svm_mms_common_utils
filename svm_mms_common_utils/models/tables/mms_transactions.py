from dataclasses import dataclass
import datetime as dt
from ...enums import TransactionStatus
from .baseTableModel import BaseTableModel


@dataclass
class MmsTransactions(BaseTableModel):
    __tablename__ = "MMS_TRANSACTIONS"

    mRID: str = None
    revision: int = 1
    status: str = TransactionStatus.PENDING
    databaseRowId: int = None
    databaseTableName: str = None
    marketDay: dt.date = None
    xmlFile: str = None
    sentXml: str = None
    receivedXml: str = None
    dateSent: dt.datetime = None
    dateReceived: dt.datetime = None
    mmsFileInterface: str = None
    xmlFileInterface: str = None
    participantId: int = None
    resourceObjectId: int = None

    def to_db(self):
        return {
            "mRID": self.mRID,
            "revision": self.revision,
            "status": self.status,
            "databaseRowId": self.databaseRowId,
            "databaseTableName": self.databaseTableName,
            "marketDay": self.marketDay.strftime("%Y-%m-%d") if self.marketDay else None,
            "xmlFile": self.xmlFile,
            "sentXml": self.sentXml,
            "receivedXml": self.receivedXml,
            "dateSent": self.dateSent.strftime("%Y-%m-%d %H:%M:%S") if self.dateSent else None,
            "dateReceived": (
                self.dateReceived.strftime("%Y-%m-%d %H:%M:%S") if self.dateReceived else None
            ),
            "mmsFileInterface": self.mmsFileInterface,
            "xmlFileInterface": self.xmlFileInterface,
            "participantId": self.participantId,
            "resourceObjectId": self.resourceObjectId,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            mRID=data["mRID"],
            revision=data["revision"],
            status=TransactionStatus[data["status"]],
            databaseRowId=data["databaseRowId"],
            databaseTableName=data["databaseTableName"],
            marketDay=(
                dt.datetime.strptime(data["marketDay"], "%Y-%m-%d").date()
                if data["marketDay"]
                else None
            ),
            xmlFile=data["xmlFile"],
            sentXml=data["sentXml"],
            receivedXml=data["receivedXml"],
            dateSent=(
                dt.datetime.strptime(data["dateSent"], "%Y-%m-%d %H:%M:%S")
                if data["dateSent"]
                else None
            ),
            dateReceived=(
                dt.datetime.strptime(data["dateReceived"], "%Y-%m-%d %H:%M:%S")
                if data["dateReceived"]
                else None
            ),
            mmsFileInterface=data["mmsFileInterface"],
            xmlFileInterface=data["xmlFileInterface"],
            participantId=data["participantId"],
            resourceObjectId=data["resourceObjectId"],
        )
