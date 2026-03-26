from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from config.permissions import IsAdminOrOperator
from companies.models import Company
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """CRUD API for external companies."""

    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes: list = [IsAdminOrOperator]

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Soft-delete: deactivate company instead of deleting."""
        company: Company = self.get_object()
        company.is_active = False
        company.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)
