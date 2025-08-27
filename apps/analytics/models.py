from django.db import models
from apps.core.models import Project, NotificationChannel

class AlertRule(models.Model):
    """Defines conditions for triggering alerts."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="alert_rules")
    name = models.CharField(max_length=100)

    METRICS = [
        ("error_count", "Error Count"),
        ("error_rate", "Error Rate"),
        ("latency", "Latency"),
        ("status_code", "Status Code"),
        ("custom", "Custom Metric"),
    ]
    metric = models.CharField(max_length=50, choices=METRICS)

    # e.g. {"status_code": 502, "threshold": 5, "window": 60}
    config = models.JSONField()

    severity = models.CharField(
        max_length=20,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="medium",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.name}"


class AlertNotification(models.Model):
    """When a rule triggers, this record is stored."""
    rule = models.ForeignKey(AlertRule, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    triggered_at = models.DateTimeField(auto_now_add=True)
    delivered_to = models.ManyToManyField(NotificationChannel, blank=True)

    def __str__(self):
        return f"Notification for {self.rule.name} at {self.triggered_at}"
