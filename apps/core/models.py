from django.db import models

import base64
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

def validate_base64_key(value):
    try:
        base64.b64decode(value, validate=True)
    except Exception:
        raise ValidationError("Invalid base64-encoded encryption key")

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    access_key = models.CharField(max_length=100, unique=True)
    encryption_key = models.CharField(
        max_length=256,
        unique=True,
        validators=[validate_base64_key, MinLengthValidator(32)],
        help_text="Base64-encoded symmetric key"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class NotificationChannel(models.Model):
    """Channels through which alerts will be sent."""
    CHANNEL_TYPES = [
        ("email", "Email"),
        ("slack", "Slack"),
        ("webhook", "Webhook"),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="channels")
    type = models.CharField(max_length=20, choices=CHANNEL_TYPES)
    config = models.JSONField(
        help_text="Channel config (email: {address}, slack: {webhook_url}, etc.)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
