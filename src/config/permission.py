from rest_framework.permissions import BasePermission

from src.apps.permissions.models import Roles


class IsAdmin(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        role = request.user.role
        if not role:
            return False
        return role.kind == Roles.KindRole.ADMIN.value
