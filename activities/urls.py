from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_activities, name='activities'),
    path('activity_page/<str:key>/', views.activity_page, name='activity_page'),
    path('add_activity/', views.add_activity, name='add_activity'),
    path('edit_activity/<str:key>/', views.edit_activity, name='edit_activity'),
    path('add_booking_slot/<str:key>/', views.add_booking_slot, name='add_booking_slot'),
    path('edit_booking_slot/<str:key>/', views.edit_booking_slot, name='edit_booking_slot'),
    path('create_booking/<str:key>/', views.create_booking, name='create_booking'),
]
