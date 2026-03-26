from rest_framework.routers import SimpleRouter

from .views import CompanyViewSet

router: SimpleRouter = SimpleRouter()
router.register("companies", CompanyViewSet, basename="company")

urlpatterns: list = router.urls
