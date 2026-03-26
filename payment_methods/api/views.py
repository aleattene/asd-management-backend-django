from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from config.permissions import IsAdminOrOperator
from payment_methods.models import PaymentMethod
from .serializers import PaymentMethodSerializer


class PaymentMethodViewSet(viewsets.ModelViewSet):
    """CRUD API for payment methods."""

    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
    permission_classes: list = [IsAdminOrOperator]

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Soft-delete: deactivate payment method instead of deleting."""
        payment_method: PaymentMethod = self.get_object()
        payment_method.is_active = False
        payment_method.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)
