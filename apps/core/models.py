from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    secret_key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name