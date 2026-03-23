from typing import Dict, List, Optional
from src.apps.permissions.dtos import RoleDataDTO
from src.apps.accounts.dtos import UserDataDTO, UserDetailedDTO
from src.apps.accounts.models import User, UserSession
from src.apps.accounts.repository import (
    UserRepository,
    UserSessionRepository,
    user_repo,
    user_session_repo,
)
from src.utils.services import AbstractService
from rest_framework_simplejwt.tokens import RefreshToken


class UserService(AbstractService[User]):
    def __init__(self, repository: UserRepository = user_repo):
        super().__init__(repository)

    def get_by_email(self, email: str) -> Optional[UserDataDTO]:
        instance = self._repository.filter(email=email).first()
        if not instance:
            return

        return UserDataDTO(
            id=instance.id,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
        )

    def get_by_id(self, id: int) -> Optional[UserDataDTO]:
        instance = self._repository.filter(id=id).first()
        if not instance:
            return

        return UserDataDTO(
            id=instance.id,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
        )

    def get_all_users(self) -> List[UserDetailedDTO]:
        instances = self._repository.all()
        return list(
            UserDetailedDTO(
                id=instance.id,
                first_name=instance.first_name,
                last_name=instance.last_name,
                email=instance.email,
                role=(
                    RoleDataDTO(id=instance.role.id, kind=instance.role.kind)
                    if instance.role
                    else None
                ),
            )
            for instance in instances
        )

    def set_password(self, email: str, password: str) -> None:
        user = self._repository.model.objects.get(email=email)
        user.set_password(password)
        user.save()

    def get_token(self, email: str) -> Dict[str, str]:
        user = self._repository.model.objects.get(email=email)
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return {
            "refresh": str(refresh),
            "access": str(access),
        }

    def check_password(self, email: str, password: str) -> bool:
        user = self._repository.model.objects.filter(
            email=email, is_active=True
        ).first()

        if not user:
            return False

        if not user.check_password(password):
            return False

        return True


class UserSessionService(AbstractService[UserSession]):
    def __init__(self, repository: UserSessionRepository = user_session_repo):
        super().__init__(repository)


user_session_service = UserSessionService()
user_service = UserService()
