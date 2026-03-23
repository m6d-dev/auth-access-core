from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import EmailStr, Field
from src.apps.permissions.dtos import RoleDataDTO
from src.utils.dto import BaseDTO


class UserDTO(BaseDTO):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserSessionDTO(BaseDTO):
    id: int
    user_id: int = Field(alias="user")
    session_id: UUID
    expires_at: datetime
    is_active: bool


class UserDataDTO(BaseDTO):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class UserDetailedDTO(UserDataDTO):
    role: Optional[RoleDataDTO]


class RegisterUserDTO(BaseDTO):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str


class RegisterAdminUserDTO(BaseDTO):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str
    role_id: int


class LoginUserDTO(BaseDTO):
    email: EmailStr
    password: str


class UpdateUserDataDTO(BaseDTO):
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
