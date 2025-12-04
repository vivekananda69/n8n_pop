from django.contrib import admin
from django.urls import path
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from workflows.views import list_workflows
from workflows.management.commands.fetch_workflows import Command as FetchCommand


def home(request):
    return JsonResponse({"message": "n8n Popularity API is running"})


def health(request):
    return JsonResponse({"status": "ok"})


@csrf_exempt
def trigger_fetch(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    secret = request.headers.get("X-Trigger-Secret")
    if secret != settings.TRIGGER_SECRET:
        return HttpResponseForbidden("Forbidden")

    try:
        FetchCommand().handle()
        return JsonResponse({"status": "fetch_started"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/workflows/", list_workflows),
    path("health/", health),
    path("trigger-fetch/", trigger_fetch),
]
