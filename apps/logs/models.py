from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    secret_key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

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
