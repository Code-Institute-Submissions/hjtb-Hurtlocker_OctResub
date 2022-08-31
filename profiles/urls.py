from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_profiles, name='profiles'),
    path('profile_page/<str:key>/', views.profile_page, name='profile_page'),
    path('edit_profile/<str:key>/', views.edit_profile, name='edit_profile'),
    path('manage_subscription', views.manage_subscription, name='manage_subscription'),
]
