import datetime as dt
from dataclasses import dataclass

from svm_mms_common_utils.enums import NonAvailabilityReason, NonAvailabilityType

from .base_table_model import BaseTableModel


@dataclass
class MmsResourceNonAvailability(BaseTableModel):
    __tablename__ = "MMS_RESOURCE_NON_AVAILABILITY"

    id: int | None
    resourceId: int
    startDate: dt.datetime
    endDate: dt.datetime
    nonAvailability: float
    reason: NonAvailabilityReason
    type: NonAvailabilityType | None = None
    status: str | None = None

    def to_db(self):
        return {
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
            reason=NonAvailabilityReason(data["reason"]),
            status=data.get("status"),
        )
