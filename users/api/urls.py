from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router: DefaultRouter = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns: list = router.urls
