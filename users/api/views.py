from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from config.permissions import IsAdminOrOperator
from users.models import CustomUser
from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserCreateSerializer,
    UserMeSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD API for user management.

    - list/create/update/delete: admin and operator only
    - me: any authenticated user can view/update their own profile
    """

    queryset = CustomUser.objects.filter(is_active=True)
    permission_classes: list = [IsAdminOrOperator]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        if self.action == "list":
            return UserListSerializer
        if self.action == "me":
            return UserMeSerializer
        return UserDetailSerializer

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Soft-delete: deactivate user instead of deleting."""
        user: CustomUser = self.get_object()
        user.is_active = False
        user.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get", "patch"], permission_classes=[IsAuthenticated])
    def me(self, request: Request) -> Response:
        """View or update the authenticated user's own profile."""
        if request.method == "GET":
            serializer = UserMeSerializer(request.user)
            return Response(serializer.data)
        serializer = UserMeSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
