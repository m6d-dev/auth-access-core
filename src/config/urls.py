from django.contrib import admin
from django.urls import path, include

from . import swagger


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/accounts/", include("src.apps.accounts.urls")),
    path("api/v1/access-rules/", include("src.apps.permissions.urls")),
]

urlpatterns += swagger.urlpatterns
