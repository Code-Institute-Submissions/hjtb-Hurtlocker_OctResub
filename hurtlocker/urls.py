from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('memberships/', include('memberships.urls')),
    path('profiles/', include('profiles.urls')),
    path('activities/', include('activities.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
