from django.urls import path
from .views import UpdateAccessRuleAPIView

urlpatterns = [
    path("all/", UpdateAccessRuleAPIView.as_view(), name="access-rules"),
]
