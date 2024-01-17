from django.conf import settings
from django.contrib import admin
from django.urls import include, path

import {{ cookiecutter.app_name }}.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", {{ cookiecutter.app_name }}.views.index),
]

if settings.DEBUG:
    urlpatterns.append(
        path("__reload__/", include("django_browser_reload.urls")),
    )
