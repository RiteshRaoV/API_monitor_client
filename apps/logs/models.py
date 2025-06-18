from django.db import models
from apps.core.models import Project
# Create your models here.

class Endpoint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='endpoints')
    path = models.CharField(max_length=255)  # e.g. /get-details/
    method = models.CharField(max_length=10)  # GET, POST, etc.
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'path', 'method')

    def __str__(self):
        return f"{self.method} {self.path}"
