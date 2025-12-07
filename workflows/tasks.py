from django.utils import timezone
from datetime import timedelta
from .models import Workflow


def save_items(items, platform, country):
    """
    items: list of dicts like:
    {
        "workflow": "Video Title",
        "source_url": "...",
        "metrics": {...},
        "score": 123.4
    }
    """
    now = timezone.now()
    for item in items:
        Workflow.objects.update_or_create(
            workflow=item["workflow"],
            platform=platform,
            country=country,
            defaults={
                "source_url": item.get("source_url", ""),
                "popularity_metrics": item.get("metrics", {}),
                "popularity_score": item.get("score", 0),
                "last_seen": now,
            },
        )


def get_cron_status():
    """
    Infer cron status from latest last_seen.
    """
    last = (
        Workflow.objects.exclude(last_seen__isnull=True)
        .order_by("-last_seen")
        .first()
    )
    if not last:
        return None, None

    last_run = last.last_seen
    next_run = last_run + timedelta(hours=6)
    return last_run, next_run
