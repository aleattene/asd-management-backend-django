"""URL configuration for ASD Management project — API-only."""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns: list = [
    # Django Admin (requires is_staff=True)
    path("admin/", admin.site.urls),
    # JWT Authentication
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # App APIs
    path("api/v1/", include("users.api.urls")),
    path("api/v1/", include("athletes.api.urls")),
    path("api/v1/", include("staff.api.urls")),
    path("api/v1/", include("doctors.api.urls")),
    path("api/v1/", include("enrollments.api.urls")),
    path("api/v1/", include("certificates.api.urls")),
    path("api/v1/", include("geography.api.urls")),
    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
