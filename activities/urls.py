from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_activities, name='activities'),
    path('activity_page/<str:key>/', views.activity_page, name='activity_page'),
    path('add_activity/', views.add_activity, name='add_activity'),
    path('edit_activity/<str:key>/', views.edit_activity, name='edit_activity'),
]
