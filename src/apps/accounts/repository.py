from src.apps.accounts.models import User, UserSession
from src.utils.repositories import AbstractRepository


class UserRepository(AbstractRepository[User]):
    model = User


class UserSessionRepository(AbstractRepository[UserSession]):
    model = UserSession


user_repo = UserRepository()
user_session_repo = UserSessionRepository()
