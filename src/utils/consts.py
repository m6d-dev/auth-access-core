from enum import StrEnum


class ViewAction(StrEnum):
    LIST = "list"
    CREATE = "create"
    RETRIEVE = "retrieve"
    UPDATE = "update"
    PARTIAL_UPDATE = "partial_update"
    DESTROY = "destroy"
