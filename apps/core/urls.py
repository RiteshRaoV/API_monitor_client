# apps/core/urls.py

from django.urls import path
from apps.core.views import ProjectListCreateAPIView

urlpatterns = [
    path('projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
]
