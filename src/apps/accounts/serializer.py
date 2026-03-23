from typing import Dict, Tuple
from rest_framework import serializers
from src.apps.accounts.dtos import (
    RegisterAdminUserDTO,
    RegisterUserDTO,
    LoginUserDTO,
    UpdateUserDataDTO,
)
from src.apps.accounts.use_cases import (
    register_uc,
    login_uc,
    user_update_data_uc,
    register_admin_uc,
)
from src.apps.permissions.services import role_service


class UserDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()


class RegisterSerialzier(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    confirm_password = serializers.CharField()

    def save(self, **kwargs) -> None:
        register_uc.execute(
            dto=RegisterUserDTO(
                first_name=self.validated_data.get("first_name"),
                last_name=self.validated_data.get("last_name"),
                email=self.validated_data.get("email"),
                password=self.validated_data.get("password"),
                confirm_password=self.validated_data.get("confirm_password"),
            )
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def save(self, **kwargs) -> Tuple[int, Dict[str, str]]:
        return login_uc.execute(
            dto=LoginUserDTO(
                email=self.validated_data.get("email"),
                password=self.validated_data.get("password"),
            )
        )


class UpdateUserDataSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    def save(self):
        user = self.context["request"].user
        dto = UpdateUserDataDTO(user_id=user.id, **self.validated_data)

        dto_res = user_update_data_uc.execute(dto=dto)
        return dto_res.model_dump()


class RegisterAdminSerialzier(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    confirm_password = serializers.CharField()

    def save(self, **kwargs) -> None:
        return register_admin_uc.execute(
            dto=RegisterAdminUserDTO(
                first_name=self.validated_data.get("first_name"),
                last_name=self.validated_data.get("last_name"),
                email=self.validated_data.get("email"),
                password=self.validated_data.get("password"),
                confirm_password=self.validated_data.get("confirm_password"),
                role_id=role_service.get_admin().id,
            )
        )
