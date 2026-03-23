import uuid
from django.db import models
from src.apps.permissions.models import Roles
from src.utils.models import CustomAbstractUser


class User(CustomAbstractUser):
    email_confirmed = models.BooleanField(default=False)
    first_name = models.CharField(verbose_name="Имя", max_length=20)
    last_name = models.CharField(verbose_name="Фамилия", max_length=20)

    role = models.ForeignKey(
        Roles, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )

    class Meta(CustomAbstractUser.Meta):
        app_label = "accounts"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    user_agent = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()

    class Meta(CustomAbstractUser.Meta):
        app_label = "accounts"
        verbose_name = "Сессия"
        verbose_name_plural = "Сессии"
