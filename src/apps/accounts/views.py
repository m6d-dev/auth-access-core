from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from src.config.permission import IsAdmin
from src.config.authentication import SessionAuthentication
from src.apps.accounts.serializer import (
    LoginSerializer,
    RegisterAdminSerialzier,
    RegisterSerialzier,
    UpdateUserDataSerializer,
)
from src.apps.accounts.use_cases import deactivate_user_uc, logout_uc
from src.utils.functions import raise_validation_error_detail
from src.apps.accounts.services import user_session_service, user_service


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={status.HTTP_200_OK: OpenApiResponse(description="Login success")},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id, token = serializer.save()
        session = user_session_service.create(
            user_id=user_id,
            expires_at=timezone.now() + timedelta(days=7),
            user_agent=request.META.get("HTTP_USER_AGENT"),
            ip=request.META.get("REMOTE_ADDR"),
        )
        response = Response(token, status=status.HTTP_200_OK)
        response.set_cookie(
            "sessionId", session.session_id, httponly=True, secure=True, samesite="Lax"
        )
        response.set_cookie(
            "refresh_token",
            token["refresh"],
            httponly=True,
            secure=True,
            samesite="Lax",
        )
        return response


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerialzier,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(description="User registered")
        },
    )
    def post(self, request):
        serializer = RegisterSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class UpdateUserAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=UpdateUserDataSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(description="User data updated")
        },
    )
    def patch(self, request):
        serializer = UpdateUserDataSerializer(
            instance=request.user,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.save(), status=status.HTTP_200_OK)


class DeactivateUserAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="User deactivated")
        },
    )
    def delete(self, request):
        if deactivate_user_uc.execute(user_id=request.user.id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise_validation_error_detail("Ошибка при удалении")


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="User logout")
        },
    )
    def post(self, request):
        logout_uc.execute(request=request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("refresh_token")
        response.delete_cookie("sessionId")
        return response


class RegisterAdminAPIView(APIView):
    @extend_schema(
        request=RegisterAdminSerialzier,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(description="User registered")
        },
    )
    def post(self, request):
        serializer = RegisterAdminSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class UsersAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = user_service.get_all_users()
        return Response([u.model_dump() for u in users])
