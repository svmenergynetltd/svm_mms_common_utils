from dataclasses import dataclass
from .baseTableModel import BaseTableModel
from svm_mms_common_utils.enums import RtbmFlowDirection


@dataclass
class MmsRtbmDispatch(BaseTableModel):
    __tablename__ = "MMS_RTBM_DISPATCH"

    id: int
    resourceId: int
    dayTimestamp: str
    dispatchInstructions: list[dict[str, str | float | None]]

    def to_db(self):
        return {
            "resourceId": self.resourceId,
            "dayTimestamp": self.dayTimestamp,
            "dispatchInstructions": self.dispatchInstructions,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            resourceId=data["resourceId"],
            dayTimestamp=data["dayTimestamp"],
            dispatchInstructions=data["dispatchInstructions"],
        )
