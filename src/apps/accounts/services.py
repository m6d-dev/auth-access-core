from typing import Dict
from src.apps.accounts.models import User
from src.apps.accounts.repository import UserRepository, user_repo
from src.utils.services import AbstractService
from rest_framework_simplejwt.tokens import RefreshToken

class UserService(AbstractService[User]):
    def __init__(self, repository: UserRepository = user_repo):
        super().__init__(repository)

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
        user = self._repository.model.objects.filter(email=email).first()

        if not user:
            return False

        if not user.check_password(password):
            return False
        
        return True

user_service = UserService()
