from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Workflow
from .serializers import WorkflowSerializer
from .tasks import get_cron_status
from django.core.management import call_command


@api_view(["GET"])
def list_workflows(request):
    platform = request.GET.get("platform")
    country = request.GET.get("country")
    limit = int(request.GET.get("limit", 100))

    qs = Workflow.objects.all()

    if platform:
        qs = qs.filter(platform__iexact=platform)
    if country:
        qs = qs.filter(country__iexact=country)

    qs = qs.order_by("-popularity_score")[: min(limit, 1000)]
    serializer = WorkflowSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def cron_status(request):
    last_run, next_run = get_cron_status()
    return Response(
        {
            "last_run": last_run,
            "next_run": next_run,
            "interval_hours": 6,
        }
    )


@csrf_exempt
def trigger_fetch(request, source, country):
    """
    Manual trigger for cron / Streamlit / GitHub Actions.

    POST /trigger/youtube/US/
    Header: X-Trigger-Secret: <TRIGGER_SECRET>
    """
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    # Secret check
    secret = request.headers.get("X-Trigger-Secret") or request.META.get(
        "HTTP_X_TRIGGER_SECRET"
    )
    if not secret or secret != getattr(settings, "TRIGGER_SECRET", ""):
        return HttpResponseForbidden("Forbidden")

    if source not in ("youtube", "forum", "trends"):
        return JsonResponse({"error": "Unknown source"}, status=400)

    try:
        call_command(f"fetch_{source}", country)
        return JsonResponse({"ok": True, "source": source, "country": country})
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)
