from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from src.apps.permissions.serializer import CreateAccessRuleSerializer
from src.config.permission import IsAdmin
from rest_framework import status
from src.apps.permissions.services import access_role_service
from drf_spectacular.utils import extend_schema, OpenApiResponse
from src.apps.permissions.models import Roles
from src.apps.permissions.serializer import RoleSerializer


class UpdateAccessRuleAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        all_rules = access_role_service.get_all_rules()
        return Response([i.model_dump() for i in all_rules])

    @extend_schema(
        request=CreateAccessRuleSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(description="Access rule created"),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Invalid data"),
        },
    )
    def post(self, request):
        role_id = request.data.get("role_id")
        element_id = request.data.get("element_id")
        byte_flag = request.data.get("byte_flag", 0)

        rule = access_role_service.create(
            role_id=role_id, element_id=element_id, byte_flag=byte_flag
        )

        return Response(rule.model_dump(), status=status.HTTP_201_CREATED)


class RolesAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        responses={
            status.HTTP_200_OK: RoleSerializer(many=True),
        },
        description="Получить список всех ролей (только для администратора)",
    )
    def get(self, request):
        roles = Roles.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=RoleSerializer,
        responses={
            status.HTTP_201_CREATED: RoleSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Invalid data"),
        },
        description="Создать новую роль (только для администратора)",
    )
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoleDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        return Roles.objects.get(pk=pk)

    @extend_schema(
        request=RoleSerializer,
        responses={
            status.HTTP_200_OK: RoleSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Invalid data"),
        },
        description="Частично обновить роль",
    )
    def patch(self, request, pk):
        role = self.get_object(pk)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="Role deleted"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Role not found"),
        },
        description="Удалить роль",
    )
    def delete(self, request, pk):
        role = self.get_object(pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
