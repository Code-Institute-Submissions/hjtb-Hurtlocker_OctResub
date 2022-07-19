from django.urls import path
from . import views


# Remove unecessary paths - they might not be required anymore or else can be moved to urls in hurtlocker
urlpatterns = [
    path('', views.index, name='home'),
    path('club/', views.club, name='club'),
    path('activities_page/', views.activities_page, name='activities'),
    path('activity_page/<str:key>/', views.activity_page, name='activity_page'),
]
