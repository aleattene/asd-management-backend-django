from rest_framework import permissions, viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from enrollments.models import Enrollment
from .serializers import EnrollmentListSerializer, EnrollmentDetailSerializer


class EnrollmentPermission(permissions.BasePermission):
    """
    - admin/operator/superadmin: full CRUD
    - trainer/member: read-only (queryset scoping handled in viewset)
    """

    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ("admin", "superadmin", "operator")


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    CRUD API for athlete enrollments.

    - admin/operator: full access to all enrollments
    - trainer: read-only, own athletes only
    - member: read-only, own guardian athletes only
    """

    permission_classes: list = [EnrollmentPermission]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Enrollment.objects.none()
        user = self.request.user
        qs = Enrollment.objects.select_related("athlete").filter(is_active=True)
        if user.role in ("admin", "superadmin", "operator"):
            return qs
        if user.role == "trainer":
            return qs.filter(athlete__trainer__user=user)
        return qs.filter(athlete__guardian=user)

    def get_serializer_class(self):
        if self.action == "list":
            return EnrollmentListSerializer
        return EnrollmentDetailSerializer

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Soft-delete: deactivate enrollment instead of deleting."""
        enrollment: Enrollment = self.get_object()
        enrollment.is_active = False
        enrollment.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)
