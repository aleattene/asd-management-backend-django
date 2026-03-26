from rest_framework.routers import SimpleRouter

from .views import ReceiptViewSet

router: SimpleRouter = SimpleRouter()
router.register("receipts", ReceiptViewSet, basename="receipt")

urlpatterns: list = router.urls
