from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from config.permissions import IsAdminOrOperatorOrReadOnly
from geography.models import Country, Province, Municipality
from .serializers import CountrySerializer, ProvinceSerializer, MunicipalitySerializer


class CountryViewSet(viewsets.ModelViewSet):
    """CRUD API for countries. Read-only for all authenticated users."""

    serializer_class = CountrySerializer
    permission_classes: list = [IsAdminOrOperatorOrReadOnly]
    search_fields: list[str] = ["name", "iso_code"]

    def get_queryset(self):
        if self.action == "list":
            return Country.objects.filter(is_active=True)
        return Country.objects.all()


class ProvinceViewSet(viewsets.ModelViewSet):
    """CRUD API for Italian provinces. Read-only for all authenticated users."""

    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes: list = [IsAdminOrOperatorOrReadOnly]
    search_fields: list[str] = ["name", "code"]


class MunicipalityViewSet(viewsets.ModelViewSet):
    """CRUD API for Italian municipalities. Supports filtering by province."""

    queryset = Municipality.objects.select_related("province").all()
    serializer_class = MunicipalitySerializer
    permission_classes: list = [IsAdminOrOperatorOrReadOnly]
    filter_backends: list = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields: list[str] = ["province"]
    search_fields: list[str] = ["name"]
