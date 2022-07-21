from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_profiles, name='profiles'),
    path('profile_page/<str:key>/', views.profile_page, name='profile_page'),
]
