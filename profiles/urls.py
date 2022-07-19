from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_profiles, name='profiles'),
    path('profile/<str:key>/', views.profile, name='profile'),
]
