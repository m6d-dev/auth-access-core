from typing import Dict
from rest_framework import serializers
from src.apps.accounts.dtos import RegisterUserDTO, LoginUserDTO
from src.apps.accounts.use_cases import register_uc, login_uc

class RegisterSerialzier(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    confirm_password = serializers.CharField()

    def save(self, **kwargs) -> Dict[str, str]:
        return register_uc.execute(
            dto=RegisterUserDTO(
                first_name=self.validated_data.get("first_name"),
                last_name=self.validated_data.get("last_name"),
                email=self.validated_data.get("email"),
                password=self.validated_data.get("password"),
                confirm_password=self.validated_data.get("confirm_password")
            )
        )

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def save(self, **kwargs) -> Dict[str, str]:
        return login_uc.execute(
            dto=LoginUserDTO(
                email=self.validated_data.get("email"),
                password=self.validated_data.get("password"),
            )
        )
