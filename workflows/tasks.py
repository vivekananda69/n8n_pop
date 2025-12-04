from workflows.models import Workflow
from django.utils import timezone

def save_items(items, platform, country):
    """
    items = list of dicts like:
    {
        "workflow": "Video Title",
        "source_url": "...",
        "metrics": {...},
        "score": 12.4
    }
    """

    for item in items:
        Workflow.objects.update_or_create(
            workflow=item["workflow"],
            platform=platform,
            country=country,
            defaults={
                "source_url": item.get("source_url", ""),
                "popularity_metrics": item.get("metrics", {}),
                "popularity_score": item.get("score", 0),
                "last_seen": timezone.now(),
            }
        )
