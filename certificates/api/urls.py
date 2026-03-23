from rest_framework.routers import SimpleRouter

from .views import SportCertificateViewSet

router: SimpleRouter = SimpleRouter()
router.register("certificates", SportCertificateViewSet, basename="certificate")

urlpatterns: list = router.urls
