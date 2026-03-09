from rest_framework import serializers

from src.apps.permissions.models import Roles


class CreateAccessRuleSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()
    element_id = serializers.IntegerField()
    byte_flag = serializers.IntegerField(required=False, default=0)

    def validate_role_id(self, value):
        if not Roles.objects.filter(id=value).exists():
            raise serializers.ValidationError("Role не существует")
        return value

    def validate_element_id(self, value):
        if not BussinessElement.objects.filter(id=value).exists():
            raise serializers.ValidationError("Business element не существует")
        return value
