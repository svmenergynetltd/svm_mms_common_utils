from dataclasses import dataclass
from ...enums import ResourceTypes


@dataclass
class ResourceObject:
    id: int
    name: str
    displayName: str
    mRID: str
    mmsId: str
    fmStrategy: float
    damStrategy: str
    participantId: int
    type: ResourceTypes

    def to_db(self):
        return {
            "id": self.id,
            "name": self.name,
            "displayName": self.displayName,
            "mRID": self.mRID,
            "mmsId": self.mmsId,
            "fmStrategy": self.fmStrategy,
            "damStrategy": self.damStrategy,
            "participantId": self.participantId,
            "type": self.type.value,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            displayName=data["displayName"],
            mRID=data["mRID"],
            mmsId=data["mmsId"],
            fmStrategy=data["fmStrategy"],
            damStrategy=data["damStrategy"],
            participantId=data["participantId"],
            type=ResourceTypes(data["type"]),
        )
