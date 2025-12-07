from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

from workflows.views import list_workflows, trigger_fetch, cron_status


def home(request):
    return JsonResponse({"message": "n8n Popularity API is running"})


def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", home),
    path("health/", health),
    path("admin/", admin.site.urls),
    path("api/workflows/", list_workflows),
    path("api/status/", cron_status),
    path("trigger/<str:source>/<str:country>/", trigger_fetch),
]
