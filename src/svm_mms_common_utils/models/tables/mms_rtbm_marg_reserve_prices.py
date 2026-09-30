from dataclasses import dataclass

from svm_mms_common_utils.enums import RtbmReserveProcessType

from .base_table_model import BaseTableModel


@dataclass
class MmsRtbmMargReservePrices(BaseTableModel):
    __tablename__ = "MMS_RTBM_MARG_RESERVE_PRICES"

    dayTimestamp: str
    processType: RtbmReserveProcessType
    marginalReservePrices: list[dict[str, str | float | None]]
    id: int | None = None

    def to_db(self):
        return {
            "dayTimestamp": self.dayTimestamp,
            "processType": self.processType,
            "marginalReservePrices": self.marginalReservePrices,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            dayTimestamp=data["dayTimestamp"],
            processType=RtbmReserveProcessType[data["processType"]],
            marginalReservePrices=data["marginalReservePrices"],
            id=data.get("id"),
        )
