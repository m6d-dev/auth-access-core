from src.apps.permissions.repository import (
    AccessRolesRuleRepository,
    RoleRepository,
    role_repo,
    access_role_repo,
)
from src.apps.permissions.dtos import RoleDataDTO, AccessRoleListDTO
from src.apps.permissions.models import AccessRolesRules, Roles
from src.utils.services import AbstractService
from typing import List


class RoleService(AbstractService[Roles]):
    def __init__(self, repository: RoleRepository = role_repo):
        super().__init__(repository)

    def get_admin(self) -> RoleDataDTO:
        instance = self._repository.get(kind=Roles.KindRole.ADMIN)
        return RoleDataDTO(id=instance.id, kind=instance.kind)


class AccessRolesRuleService(AbstractService[AccessRolesRules]):
    def __init__(self, repository: AccessRolesRuleRepository = access_role_repo):
        super().__init__(repository)

    def get_all_rules(self) -> List[AccessRoleListDTO]:
        instances = self._repository.all()

        return [
            AccessRoleListDTO(
                id=inst.id, role=inst.kind, element=inst.role, byte_flag=inst.byte_flag
            )
            for inst in instances
        ]


role_service = RoleService()
access_role_service = AccessRolesRuleService()
