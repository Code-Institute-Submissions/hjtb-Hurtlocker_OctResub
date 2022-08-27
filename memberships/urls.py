from django.urls import path
from . import views


urlpatterns = [
    path('membership_signup', views.membership_signup, name='membership_signup'),
    path('checkout', views.checkout, name='checkout'),
]
