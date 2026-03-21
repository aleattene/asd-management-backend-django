from rest_framework import permissions, viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from config.permissions import IsAdminOrOperatorOrReadOnly
from athletes.models import Athlete, Category
from .serializers import AthleteListSerializer, AthleteDetailSerializer, CategorySerializer


class AthletePermission(permissions.BasePermission):
    """
    - admin/operator: full CRUD
    - trainer/member: read-only (filtered queryset handles scoping)
    """

    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ("admin", "superadmin", "operator")


class AthleteViewSet(viewsets.ModelViewSet):
    """
    CRUD API for athletes.

    - admin/operator: full access to all athletes
    - trainer: read-only access to own athletes
    - member: read-only access to own guardian athletes
    """

    permission_classes: list = [AthletePermission]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Athlete.objects.none()
        user = self.request.user
        qs = Athlete.objects.select_related("category", "trainer", "guardian").filter(is_active=True)
        if user.role in ("admin", "superadmin", "operator"):
            return qs
        if user.role == "trainer":
            return qs.filter(trainer__user=user)
        return qs.filter(guardian=user)

    def get_serializer_class(self):
        if self.action == "list":
            return AthleteListSerializer
        return AthleteDetailSerializer

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Soft-delete: deactivate athlete instead of deleting."""
        athlete: Athlete = self.get_object()
        athlete.is_active = False
        athlete.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD API for athlete categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes: list = [IsAdminOrOperatorOrReadOnly]
