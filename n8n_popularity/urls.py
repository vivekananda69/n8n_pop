from django.contrib import admin
from django.urls import path
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from workflows.management.commands.fetch_once import Command as FetchOnceCommand

def trigger_fetch(request, source, country):
    secret = request.headers.get("X-Trigger-Secret")
    if secret != settings.TRIGGER_SECRET:
        return HttpResponseForbidden("Forbidden")

    try:
        FetchOnceCommand().handle(source=source, country=country)
        return JsonResponse({"status": "ok", "source": source, "country": country})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/workflows/", list_workflows),
    path("", home),
    path("health/", health),
    path("trigger-fetch/<str:source>/<str:country>/", trigger_fetch),
]
