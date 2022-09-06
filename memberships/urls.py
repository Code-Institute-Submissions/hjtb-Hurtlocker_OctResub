from django.urls import path
from . import views
from .webhooks import webhooks


urlpatterns = [
    path('membership_signup', views.membership_signup, name='membership_signup'),
    path('checkout', views.checkout, name='checkout'),
    path('create_checkout_session', views.create_checkout_session, name='create_checkout_session'),
    path('checkout_success', views.checkout_success, name='checkout_success'),
    path('subscription_cancelled', views.subscription_cancelled, name='subscription_cancelled'),
    path('webhooks', webhooks, name='webhooks'),
]
