from django.urls import path
from .views import (
    DeactivateUserAPIView,
    LoginAPIView,
    RegisterAPIView,
    RegisterAdminAPIView,
    UpdateUserAPIView,
    UserLogoutAPIView,
    UsersAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("update/", UpdateUserAPIView.as_view(), name="update_user"),
    path("delete/", DeactivateUserAPIView.as_view(), name="delete_user"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout"),
    path("register/admin/", RegisterAdminAPIView.as_view(), name="register-admin"),
    path("users/", UsersAPIView.as_view(), name="users"),
]
