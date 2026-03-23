from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, username, password=None, **extra_fields):
        from src.apps.accounts.models import User

        """Create and save a User with the given username and password."""
        if not username:
            raise ValueError("The given username must be set")
        user: "User" = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create(self, username, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)
