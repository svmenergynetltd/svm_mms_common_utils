from enum import Enum


class BaseEnum(str, Enum):
    def __get__(self, instance, owner):
        return self.value


class TransactionStatus(BaseEnum):
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"
