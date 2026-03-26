from rest_framework.routers import SimpleRouter

from .views import PaymentMethodViewSet

router: SimpleRouter = SimpleRouter()
router.register("payment-methods", PaymentMethodViewSet, basename="payment-method")

urlpatterns: list = router.urls
