from src.apps.accounts.serializer import LoginSerializer, RegisterSerialzier
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework import status

class RegisterAPIView(APIView):
    serializer_class = RegisterSerialzier
    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        request=RegisterSerialzier,
        responses={status.HTTP_200_OK: OpenApiResponse(description="Registred User")},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response(data=token, status=status.HTTP_200_OK)

class LoginAPIView(APIView):
    serializer = LoginSerializer
    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        request=LoginSerializer,
        responses={status.HTTP_201_CREATED},
    )
    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response(token, status=status.HTTP_200_OK)

