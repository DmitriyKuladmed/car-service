from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path("", TemplateView.as_view(template_name="basis/first_page.html"), name="first"),
    path("auto_service/", include("autoservice_app.urls")),
    path("admin/", admin.site.urls),
    path("", include('rest_framework.urls')),
]

