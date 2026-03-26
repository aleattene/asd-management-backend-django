from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from config.permissions import IsAdminOrOperator
from invoices.models import Invoice
from .serializers import InvoiceListSerializer, InvoiceDetailSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    """CRUD API for invoices."""

    queryset = Invoice.objects.select_related("company", "payment_method").filter(
        is_active=True
    )
    permission_classes: list = [IsAdminOrOperator]

    def get_serializer_class(self):
        if self.action == "list":
            return InvoiceListSerializer
        return InvoiceDetailSerializer

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Soft-delete: deactivate invoice instead of deleting."""
        invoice: Invoice = self.get_object()
        invoice.is_active = False
        invoice.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)
