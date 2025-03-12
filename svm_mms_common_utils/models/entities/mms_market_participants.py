from dataclasses import dataclass
import datetime as dt


@dataclass
class MarketParticipant:
    id: int
    mRID: str
    participantName: str
    participantDisplayName: str
    mainFunction: int
    fmStrategy: float
    managedBy: str
    mmsId: str

    dateAdded: dt.datetime
    dateModified: dt.datetime
    isActive: bool = True

    def to_db(self):
        return {
            "id": self.id,
            "mRID": self.mRID,
            "participantName": self.participantName,
            "participantDisplayName": self.participantDisplayName,
            "mainFunction": self.mainFunction,
            "fmStrategy": self.fmStrategy,
            "managedBy": self.managedBy,
            "mmsId": self.mmsId,
            "dateAdded": self.dateAdded.strftime("%Y-%m-%d %H:%M:%S") if self.dateAdded else None,
            "dateModified": (
                self.dateModified.strftime("%Y-%m-%d %H:%M:%S") if self.dateModified else None
            ),
            "isActive": 1 if self.isActive else 0,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            mRID=data["mRID"],
            participantName=data["participantName"],
            participantDisplayName=data["participantDisplayName"],
            mainFunction=data["mainFunction"],
            fmStrategy=data["fmStrategy"],
            managedBy=data["managedBy"],
            mmsId=data["mmsId"],
            dateAdded=data["dateAdded"],
            dateModified=data["dateModified"],
            isActive=True if data["isActive"] else False,
        )
