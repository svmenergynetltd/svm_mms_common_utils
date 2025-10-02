from dataclasses import dataclass
import datetime as dt

from .baseTableModel import BaseTableModel
from svm_mms_common_utils.enums import NonAvailabilityType, NonAvailabilityReason


@dataclass
class MmsResourceNonAvailability(BaseTableModel):
    __tablename__ = "MMS_RESOURCE_NON_AVAILABILITY"

    id: int
    resourceId: int
    dateRangeStart: dt.datetime
    dateRangeEnd: dt.datetime
    nonAvailability: dict[str, str | float | None]
    type: NonAvailabilityType
    reason: NonAvailabilityReason
    status: str = None

    def to_db(self):
        return {
            "id": self.id,
            "resourceId": self.resourceId,
            "dateRangeStart": self.dateRangeStart.isoformat() if self.dateRangeStart else None,
            "dateRangeEnd": self.dateRangeEnd.isoformat() if self.dateRangeEnd else None,
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
            dateRangeStart=data["dateRangeStart"],
            dateRangeEnd=data["dateRangeEnd"],
            nonAvailability=data["nonAvailability"],
            type=NonAvailabilityType.from_name(data["type"]),
            reason=NonAvailabilityReason.from_name(data["reason"]),
            status=data.get("status"),
        )
