from src.utils.dto import BaseDTO


class RoleDataDTO(BaseDTO):
    id: int
    kind: int


class AccessRoleListDTO(BaseDTO):
    id: int
    role: str
    element: str
    byte_flag: int
