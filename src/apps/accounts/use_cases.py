from typing import Dict, Optional
from src.apps.accounts.services import user_session_service
from rest_framework.request import Request
from src.apps.accounts.services import UserService, UserSessionService
from src.apps.accounts.dtos import (
    LoginUserDTO,
    RegisterAdminUserDTO,
    RegisterUserDTO,
    UpdateUserDataDTO,
    UserDataDTO,
)
from src.apps.accounts.services import user_service
from rest_framework.exceptions import AuthenticationFailed
from src.utils.functions import raise_validation_error_detail
from django.db.transaction import atomic
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout


class RegisterUseCase:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    @atomic
    def execute(self, dto: RegisterUserDTO) -> None:
        if self._user_service.exists(email=dto.email):
            raise_validation_error_detail("Пользователь с данной почтой существует")

        if dto.password != dto.confirm_password:
            raise_validation_error_detail("Пароли не совподают")

        self._user_service.create(
            first_name=dto.first_name, last_name=dto.last_name, email=dto.email
        )

        self._user_service.set_password(email=dto.email, password=dto.password)


class LoginUseCase:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    @atomic
    def execute(self, dto: LoginUserDTO) -> Dict[str, str]:
        self._check_password(email=dto.email, password=dto.password)
        return self._user_service.get_by_email(
            email=dto.email
        ).id, self._user_service.get_token(email=dto.email)

    def _check_password(self, email: str, password: str) -> None:
        if not self._user_service.check_password(email=email, password=password):
            raise AuthenticationFailed(
                "Не найдено активной учетной записи с указанными данными"
            )


class UpdateUserDataUseCase:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    @atomic
    def execute(self, dto: UpdateUserDataDTO) -> Optional[UserDataDTO]:
        update_fields = {
            k: v
            for k, v in dto.model_dump(exclude_unset=True).items()
            if k != "user_id"
        }

        if self._user_service.update(filters={"id": dto.user_id}, **update_fields) != 1:
            raise_validation_error_detail("Ошибка при обновлении")

        return self._user_service.get_by_id(id=dto.user_id)


class DeactivateUserUseCase:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    @atomic
    def execute(self, user_id: int) -> bool:
        return (
            True
            if self._user_service.update(filters={"id": user_id}, is_active=False) == 1
            else False
        )


class LogoutUseCase:
    def __init__(self, user_session_service: UserSessionService):
        self._user_session_service = user_session_service

    @atomic
    def execute(self, request: Request) -> None:
        cookie = request._request.COOKIES
        self._user_session_service.delete({"user_id": request.user.id})
        refresh = cookie.get("refresh_token")
        if refresh:
            RefreshToken(refresh).blacklist()
        logout(request)


class RegisterAdminUseCase:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    @atomic
    def execute(self, dto: RegisterAdminUserDTO) -> None:
        if self._user_service.exists(email=dto.email):
            raise_validation_error_detail("Пользователь с данной почтой существует")

        if dto.password != dto.confirm_password:
            raise_validation_error_detail("Пароли не совподают")

        self._user_service.create(
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email,
            role_id=dto.role_id,
        )

        self._user_service.set_password(email=dto.email, password=dto.password)


login_uc = LoginUseCase(user_service=user_service)
register_uc = RegisterUseCase(user_service=user_service)
user_update_data_uc = UpdateUserDataUseCase(user_service=user_service)
deactivate_user_uc = DeactivateUserUseCase(user_service=user_service)
logout_uc = LogoutUseCase(user_session_service=user_session_service)
register_admin_uc = RegisterAdminUseCase(user_service=user_service)
