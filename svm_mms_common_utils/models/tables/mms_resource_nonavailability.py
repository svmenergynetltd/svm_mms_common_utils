from dataclasses import dataclass
import datetime as dt

from .baseTableModel import BaseTableModel
from svm_mms_common_utils.enums import NonAvailabilityType, NonAvailabilityReason


@dataclass
class MmsResourceNonAvailability(BaseTableModel):
    __tablename__ = "MMS_RESOURCE_NON_AVAILABILITY"

    id: int
    resourceId: int
    startDate: dt.datetime
    endDate: dt.datetime
    nonAvailability: float
    type: NonAvailabilityType
    reason: NonAvailabilityReason
    status: str = None

    def to_db(self):
        return {
            "id": self.id,
            "resourceId": self.resourceId,
            "startDate": self.startDate.isoformat() if self.startDate else None,
            "endDate": self.endDate.isoformat() if self.endDate else None,
            "nonAvailability": self.nonAvailability,
            "type": self.type,
            "reason": self.reason,
            "status": self.status,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            resourceId=data["resourceId"],
            startDate=data["startDate"],
            endDate=data["endDate"],
            nonAvailability=data["nonAvailability"],
            type=NonAvailabilityType.from_name(data["type"]),
            reason=NonAvailabilityReason.from_name(data["reason"]),
            status=data.get("status"),
        )
