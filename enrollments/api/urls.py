from rest_framework.routers import SimpleRouter

from .views import EnrollmentViewSet

router: SimpleRouter = SimpleRouter()
router.register("enrollments", EnrollmentViewSet, basename="enrollment")

urlpatterns: list = router.urls
