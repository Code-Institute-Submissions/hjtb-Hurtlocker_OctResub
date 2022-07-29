from django.urls import path
from . import views


urlpatterns = [
    path('', views.club_page, name='club_page'),
]
