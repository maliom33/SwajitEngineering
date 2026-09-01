from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    message = 'Your role is not authorized for this action.'

    def has_permission(self, request, view):
        required_roles = getattr(view, 'required_roles', [])
        return bool(
            request.user.is_authenticated
            and request.user.role
            and request.user.role.role_code in required_roles
        )


class HasPermission(BasePermission):
    message = 'You do not have the required permission.'

    def has_permission(self, request, view):
        permission_code = getattr(view, 'required_permission', None)
        if not request.user.is_authenticated or not request.user.role or not permission_code:
            return False
        return request.user.role.role_permissions.filter(
            permission__permission_code=permission_code,
        ).exists()


class IsSystemAdmin(BasePermission):
    message = 'System administrator access is required.'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.role
            and request.user.role.role_code == 'SYSTEM_ADMIN'
        )