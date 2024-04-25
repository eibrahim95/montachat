from django.urls import path
from .views import PublicSpectacularAPIView, PublicSpectacularSwaggerView

urlpatterns = [
    path("schema/", PublicSpectacularAPIView.as_view(), name="api-schema"),
    path(
        "docs/",
        PublicSpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    )
]
