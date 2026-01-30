from src.apps.accounts.dtos import RegisterUserDTO, UserDTO
from src.apps.accounts.models import User
from src.utils.repositories import AbstractRepository


class UserRepository(AbstractRepository[User]):
    model = User
    dto_class = UserDTO


user_repo = UserRepository()
