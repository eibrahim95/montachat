from django.shortcuts import render
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


class PublicSpectacularAPIView(SpectacularAPIView):
    authentication_classes = ()
    permission_classes = ()


class PublicSpectacularSwaggerView(SpectacularSwaggerView):
    authentication_classes = ()
    permission_classes = ()
