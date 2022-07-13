from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('club/', views.club, name='club'),
    path('activity/', views.activity, name='activity'),
    path('profile/', views.profile, name='profile'),
]
