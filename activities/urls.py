from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_activities, name='activities'),
    path('activity_page/<str:key>/', views.activity_page, name='activity_page'),
]
