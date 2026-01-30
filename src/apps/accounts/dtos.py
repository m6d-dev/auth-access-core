from pydantic import EmailStr
from src.utils.dto import BaseDTO


class UserDTO(BaseDTO):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class RegisterUserDTO(BaseDTO):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str

class LoginUserDTO(BaseDTO):
    email: EmailStr
    password: str
