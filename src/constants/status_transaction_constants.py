from enum import Enum


class StatusTransaction(Enum):
    CREATE = "CREATE"
    CONFIRM = "CONFIRM"
    VERIFY = "VERIFY"
    CANCEL = "CANCEL"
    EXPIRE = "EXPIRE"
    SUCCESS = "SUCCESS"
