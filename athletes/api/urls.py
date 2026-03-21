from rest_framework.routers import SimpleRouter

from .views import AthleteViewSet, CategoryViewSet

router: SimpleRouter = SimpleRouter()
router.register("athletes", AthleteViewSet, basename="athlete")
router.register("categories", CategoryViewSet, basename="category")

urlpatterns: list = router.urls
