from django.urls import path

from apps.logs.views import TestPackage


urlpatterns = [
    path("logs/",TestPackage.as_view())
]
