from django.db import models


class BussinessElement(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название объекта"
    )
    code = models.CharField(
        max_length=50, unique=True, verbose_name="Уникальный код объекта"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание объекта"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Объект приложения"
        verbose_name_plural = "Объекты приложения"

    def __str__(self):
        return self.name


class Roles(models.Model):
    class KindRole(models.IntegerChoices):
        ADMIN = 0, "Админ"
        MANAGER = 1, "Менеджер"
        USER = 2, "Пользователь"
        GUEST = 3, "Гость"

    kind = models.SmallIntegerField(
        verbose_name="Тип роли", choices=KindRole.choices, unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccessRolesRules(models.Model):
    """
    Таблица прав доступа через битовые флаги.
    Каждое число (byte_flag) описывает права для роли на конкретный объект (BussinessElement)
    """

    role = models.ForeignKey(
        Roles, on_delete=models.CASCADE, related_name="access_rules"
    )
    element = models.ForeignKey(
        BussinessElement, on_delete=models.CASCADE, related_name="access_rules"
    )
    byte_flag = models.IntegerField(verbose_name="Битовый флаг")

    class Meta:
        verbose_name = "Правило доступа"
        verbose_name_plural = "Правила доступа"
        unique_together = ("role", "element")

    def __str__(self):
        return f"{self.role} → {self.element} : {bin(self.byte_flag)}"

    # === Константы битов для CRUD ===
    READ_OWN = 0b0000001
    READ_ALL = 0b0000010
    CREATE = 0b0000100
    UPDATE_OWN = 0b0001000
    UPDATE_ALL = 0b0010000
    DELETE_OWN = 0b0100000
    DELETE_ALL = 0b1000000

    # === Проверка прав на объект ===
    def has_permission(self, perm_bit: int) -> bool:
        return bool(self.byte_flag & perm_bit)
