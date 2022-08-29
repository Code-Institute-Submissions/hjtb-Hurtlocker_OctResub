from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe

from profiles.models import Profile

@require_POST
@csrf_exempt
class Stripe_Webhook_Handler:
    """
    Handle webhooks from Stripe
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle random webhook events
        """
        return HttpResponse(
            content=f"Unexpected webhook received: {event['type']}", status=200
        )

    def handle_checkout_success(self, event):
        """
        A view to handle checkout success
        """
        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # try:
            #     stripe.api_key = settings.STRIPE_SECRET_KEY
            # except Exception as e:
            #     return JsonResponse({'error': (e.args[0])}, status=403)
            #     print(e)

            # # Fetch all the required data from session
            # customer = session.customer
            # subscription = session.subscription
            # current_profile.is_subscribed = True
            # current_profile.stripe_customer_id = customer.id
            # current_profile.stripe_subscription_id = subscription.id
            # try:
            #     current_profile.save()
            # except Exception as e:
            #     print(e)
            #     return JsonResponse({'error': (e.args[0])}, status=403)
            # print(current_profile.user + ' just subscribed.')

    def handle_payment_succeeded(self, event):
        """
        Handle invoice.payment_succeeded webhook from stripe
        """
        return HttpResponse(
            content=f"Webhook received: {event['type']}", status=200
        )

    def handle_payment_failed(self, event):
        """
        Handle invoice.payment_failed webhook from stripe
        """
        return HttpResponse(
            content=f"Webhook received: {event['type']}", status=200
        )