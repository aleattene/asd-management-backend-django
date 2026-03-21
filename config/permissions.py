from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsRoleAdminOrSuperadmin(permissions.BasePermission):
    """Allows access only to users with role admin or superadmin."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ("admin", "superadmin")


class IsAdminOrOperator(permissions.BasePermission):
    """Allows access to admin, superadmin, and operator roles."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ("admin", "superadmin", "operator")


class IsTrainer(permissions.BasePermission):
    """Allows access only to users with trainer role."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == "trainer"


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allows read-only access to any authenticated user, write access to admin/operator."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ("admin", "superadmin", "operator")
