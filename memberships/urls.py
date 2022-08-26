from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_memberships, name='memberships'),
    path('membership_page/<str:key>/',
         views.membership_page, name='membership_page'),
    path('membership_signup', views.membership_signup, name='membership_signup'),
    path('checkout', views.checkout, name='checkout'),
    path('config/', views.stripe_config),
]
