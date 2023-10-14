from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('django/admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
]
