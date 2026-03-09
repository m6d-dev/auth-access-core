from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from src.apps.permissions.serializer import CreateAccessRuleSerializer
from src.config.permission import IsAdmin
from rest_framework import status
from src.apps.permissions.services import access_role_service
from drf_spectacular.utils import extend_schema, OpenApiResponse


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
