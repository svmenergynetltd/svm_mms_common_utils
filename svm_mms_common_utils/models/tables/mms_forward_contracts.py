from dataclasses import dataclass
import datetime as dt
from svm_mms_common_utils.enums import ContractStatus


@dataclass
class MmsForwardContract:
    id: int
    inParticipantId: int
    outParticipantId: int
    marketAgreementMRID: str
    dayTimestamp: dt.date
    forwardContract: list[dict[str, str | float | None]]
    totalDayEnergy: float
    status: ContractStatus
    createdBy: str

    def to_db(self):
        return {
            "id": self.id,
            "inParticipantId": self.inParticipantId,
            "outParticipantId": self.outParticipantId,
            "marketAgreementMRID": self.marketAgreementMRID,
            "dayTimestamp": self.dayTimestamp.strftime("%Y-%m-%d"),
            "forwardContract": self.forwardContract,
            "totalDayEnergy": round(self.totalDayEnergy, 3),
            "status": self.status,
            "createdBy": self.createdBy,
        }

    @classmethod
    def from_db(cls, data: dict):
        return cls(
            id=data["id"],
            inParticipantId=data["inParticipantId"],
            outParticipantId=data["outParticipantId"],
            marketAgreementMRID=data["marketAgreementMRID"],
            dayTimestamp=data["dayTimestamp"],
            forwardContract=data["forwardContract"],
            totalDayEnergy=data["totalDayEnergy"],
            status=ContractStatus[data["status"]],
            createdBy=data["createdBy"],
        )
