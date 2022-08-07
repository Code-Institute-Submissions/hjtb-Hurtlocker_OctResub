from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_memberships, name='memberships'),
    path('membership_page/<str:key>/',
         views.membership_page, name='membership_page'),
    path('membership_signup', views.membership_signup, name='membership_signup'),
]
