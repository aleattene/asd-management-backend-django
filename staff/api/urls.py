from rest_framework.routers import SimpleRouter

from .views import TrainerViewSet, SportDoctorViewSet

router: SimpleRouter = SimpleRouter()
router.register("trainers", TrainerViewSet, basename="trainer")
router.register("doctors", SportDoctorViewSet, basename="doctor")

urlpatterns: list = router.urls
