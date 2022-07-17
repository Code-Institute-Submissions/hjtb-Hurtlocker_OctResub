from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('club/', views.club, name='club'),
    path('activities_page/', views.activities_page, name='activities'),
    path('activity_page/<str:key>/', views.activity_page, name='activity_page'),
    path('profile/<str:key>/', views.profile, name='profile'),
]
