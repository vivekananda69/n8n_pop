# workflows/tasks.py
from django.utils import timezone
from workflows.models import Workflow

def save_items(items):
    """
    Generic saver for YouTube, Forum, GoogleTrends.
    Each item must contain:
      - workflow (string)
      - platform (string)
      - country (string)
      - metrics (dict)
      - score (float)
      - source_url (string)
    """

    for item in items:
        Workflow.objects.update_or_create(
            workflow=item["workflow"],
            platform=item["platform"],   # comes from collectors
            country=item["country"],     # comes from collectors
            defaults={
                "source_url": item.get("source_url", ""),
                "popularity_metrics": item.get("metrics", {}),
                "popularity_score": item.get("score", 0),
                "last_seen": timezone.now(),
            }
        )
