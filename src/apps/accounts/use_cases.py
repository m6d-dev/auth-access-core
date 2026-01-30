from typing import Dict
from src.apps.accounts.services import UserService
from src.apps.accounts.dtos import LoginUserDTO, RegisterUserDTO
from src.apps.accounts.models import User
from src.apps.accounts.services import user_service
from rest_framework.exceptions import AuthenticationFailed
from src.utils.functions import raise_validation_error_detail
from django.db.transaction import atomic


class RegisterUseCase:
    def __init__(
        self,
        user_service: UserService
    ):
        self._user_service = user_service

    @atomic
    def execute(self, dto: RegisterUserDTO) -> Dict[str, str]:
        if self._user_service.exists(email=dto.email):
            raise_validation_error_detail("Пользователь с данной почтой существует")

        if dto.password != dto.confirm_password:
            raise_validation_error_detail("Пароли не совподают")

        self._user_service.create(
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email
        )

        self._user_service.set_password(email=dto.email, password=dto.password)

        return self._user_service.get_token(email=dto.email)

class LoginUseCase:
    def __init__(
        self,
        user_service: UserService
    ):
        self._user_service = user_service

    def execute(self, dto: LoginUserDTO) -> User:
        self._check_password(email=dto.email, password=dto.password)
        return self._user_service.get_token(email=dto.email)

    def _check_password(self, email: str, password: str) -> None:
        if not self._user_service.check_password(email=email, password=password):
            raise AuthenticationFailed(
                "Не найдено активной учетной записи с указанными данными"
            )

login_uc = LoginUseCase(
    user_service=user_service
)
register_uc = RegisterUseCase(
    user_service=user_service
)