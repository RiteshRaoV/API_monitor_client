# apps/core/urls.py

from django.urls import path
from apps.core.v1.Project_APIs.project_api import EndpointListView, ProjectListCreateAPIView

urlpatterns = [
    path('projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('endpoints/',EndpointListView.as_view())
]
