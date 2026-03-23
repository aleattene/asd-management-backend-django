from rest_framework.routers import SimpleRouter

from .views import CountryViewSet, ProvinceViewSet, MunicipalityViewSet

router: SimpleRouter = SimpleRouter()
router.register("countries", CountryViewSet, basename="country")
router.register("provinces", ProvinceViewSet, basename="province")
router.register("municipalities", MunicipalityViewSet, basename="municipality")

urlpatterns: list = router.urls
