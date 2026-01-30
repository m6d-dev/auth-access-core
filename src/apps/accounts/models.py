from django.db import models
from src.apps.accounts.manager import UserManager
from src.utils.models import CustomAbstractUser


class User(CustomAbstractUser):
    email_confirmed = models.BooleanField(default=False)
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=20
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=20
    )

    # objects = UserManager()

    class Meta(CustomAbstractUser.Meta):
        app_label = "accounts"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
