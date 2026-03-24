from django.urls import path
from .views import RoleDetailAPIView, RolesAPIView, UpdateAccessRuleAPIView

urlpatterns = [
    path("all/", UpdateAccessRuleAPIView.as_view(), name="access-rules"),
    path("roles/", RolesAPIView.as_view()),
    path("roles/<int:pk>/", RoleDetailAPIView.as_view()),
]
