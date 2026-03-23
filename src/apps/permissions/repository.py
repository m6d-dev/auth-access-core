from src.apps.permissions.models import AccessRolesRules, Roles
from src.utils.repositories import AbstractRepository


class RoleRepository(AbstractRepository[Roles]):
    model = Roles


class AccessRolesRuleRepository(AbstractRepository[AccessRolesRules]):
    model = AccessRolesRules


role_repo = RoleRepository()
access_role_repo = AccessRolesRuleRepository()
