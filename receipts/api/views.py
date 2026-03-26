from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from config.permissions import IsAdminOrOperator
from receipts.models import Receipt
from .serializers import ReceiptListSerializer, ReceiptDetailSerializer


class ReceiptViewSet(viewsets.ModelViewSet):
    """CRUD API for receipts."""

    queryset = Receipt.objects.select_related("user", "payment_method").filter(
        is_active=True
    )
    permission_classes: list = [IsAdminOrOperator]

    def get_serializer_class(self):
        if self.action == "list":
            return ReceiptListSerializer
        return ReceiptDetailSerializer

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Soft-delete: deactivate receipt instead of deleting."""
        receipt: Receipt = self.get_object()
        receipt.is_active = False
        receipt.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)
