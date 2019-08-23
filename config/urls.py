from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view()

urlpatterns = [
    path('', schema_view),
    path('v1', include('v1.urls')),
    path('admin/', admin.site.urls),
]
