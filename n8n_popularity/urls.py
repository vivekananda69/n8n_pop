from django.contrib import admin
from django.urls import path
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt

from workflows.views import list_workflows

def home(request):
    return JsonResponse({"message": "n8n Popularity API is running"})


def health(request):
    return JsonResponse({"status": "ok"})


@csrf_exempt                     # ✅ REQUIRED
def trigger_fetch(request, source, country):
    secret = request.headers.get("X-Trigger-Secret")
    if secret != settings.TRIGGER_SECRET:
        return HttpResponseForbidden("Forbidden")

    try:
        call_command(f"fetch_{source}", country)
        return JsonResponse({"ok": True, "source": source, "country": country})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/workflows/", list_workflows),
    path("health/", health),
    path("trigger/<str:source>/<str:country>/", trigger_fetch),
]
