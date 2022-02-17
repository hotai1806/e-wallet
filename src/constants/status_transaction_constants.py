from enum import Enum


class StatusTransaction(Enum):
    INITIALIZED = "INITIALIZED"
    CONFIRMED = "CONFIRMED"
    VERIFYED = "VERIFYED"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
