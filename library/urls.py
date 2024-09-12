"""
Main URLs module that dynamically loads frontend or admin URLs based on the API_NAME setting
"""
from django.conf import settings
from django.urls import include, path

if settings.API_NAME == "frontend-api":
    urlpatterns = [
        path('', include("library.endpoints.frontend_urls")),
    ]
elif settings.API_NAME == "admin-api":
    urlpatterns = [
        path('', include("library.endpoints.admin_urls")),
    ]
else:
    raise ValueError(f"Invalid API_NAME: {settings.API_NAME}. It must be 'frontend-api' or 'admin-api'.")
