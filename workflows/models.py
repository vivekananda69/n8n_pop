from django.db import models


class Workflow(models.Model):
    PLATFORM_CHOICES = [
        ("YouTube", "YouTube"),
        ("Forum", "Forum"),
        ("GoogleTrends", "GoogleTrends"),
    ]

    workflow = models.CharField(max_length=500)
    platform = models.CharField(max_length=32, choices=PLATFORM_CHOICES)
    country = models.CharField(max_length=8)

    source_url = models.URLField(max_length=1000, blank=True)

    popularity_metrics = models.JSONField(default=dict, blank=True)
    popularity_score = models.FloatField(default=0)

    last_seen = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("workflow", "platform", "country")
        ordering = ["-popularity_score"]

    def __str__(self):
        return f"{self.workflow} [{self.platform}/{self.country}]"
