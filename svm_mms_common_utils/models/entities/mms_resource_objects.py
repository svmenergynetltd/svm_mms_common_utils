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
    damStrategyHolidays: str
    rtbmStrategy: str
    rtbmStrategyHolidays: str
    rtbmBalEnergyOffers: str
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
            "damStrategyHolidays": self.damStrategyHolidays,
            "rtbmStrategy": self.rtbmStrategy,
            "rtbmStrategyHolidays": self.rtbmStrategyHolidays,
            "rtbmBalEnergyOffers": self.rtbmBalEnergyOffers,
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
            damStrategyHolidays=data["damStrategyHolidays"],
            rtbmStrategy=data["rtbmStrategy"],
            rtbmStrategyHolidays=data["rtbmStrategyHolidays"],
            rtbmBalEnergyOffers=data["rtbmBalEnergyOffers"],
            participantId=data["participantId"],
            type=ResourceTypes(data["type"]),
        )
