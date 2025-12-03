from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from workflows.views import list_workflows


def home(request):
    return JsonResponse({"message": "n8n Popularity API is running"})


def health(request):
    return JsonResponse({"status": "ok"}, status=200)


urlpatterns = [
    path("", home), 
    path("admin/", admin.site.urls),
    path("api/workflows/", list_workflows),
    path("health", health),
]
