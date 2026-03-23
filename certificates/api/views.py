from rest_framework import permissions, viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from certificates.models import SportCertificate
from .serializers import SportCertificateListSerializer, SportCertificateDetailSerializer


class CertificatePermission(permissions.BasePermission):
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


class SportCertificateViewSet(viewsets.ModelViewSet):
    """
    CRUD API for sport medical certificates.

    - admin/operator: full access to all certificates
    - trainer: read-only, own athletes only
    - member: read-only, own guardian athletes only
    """

    permission_classes: list = [CertificatePermission]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return SportCertificate.objects.none()
        user = self.request.user
        qs = SportCertificate.objects.select_related("athlete", "doctor").filter(is_active=True)
        if user.role in ("admin", "superadmin", "operator"):
            return qs
        if user.role == "trainer":
            return qs.filter(athlete__trainer__user=user)
        return qs.filter(athlete__guardian=user)

    def get_serializer_class(self):
        if self.action == "list":
            return SportCertificateListSerializer
        return SportCertificateDetailSerializer

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Soft-delete: deactivate certificate instead of deleting."""
        cert: SportCertificate = self.get_object()
        cert.is_active = False
        cert.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)
