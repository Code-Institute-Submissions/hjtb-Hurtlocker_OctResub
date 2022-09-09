from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe
from .webhook_handler import Stripe_Webhook_Handler


@require_POST
@csrf_exempt
def webhooks(request):
    """
    A view to handle webhooks from stripe
    """

    wh_secret = settings.STRIPE_ENDPOINT_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload 
        return HttpResponse(content=e, status=400)

    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(content=e, status=400)

    except Exception as e:
        return HttpResponse(content=e, status=400)

    handler = Stripe_Webhook_Handler(request)

    event_map = {
        'customer.subscription.updated': handler.handle_subscription_updated,
        'invoice.paid': handler.handle_payment_succeeded,
        'invoice.payment_failed': handler.handle_payment_failed,
    }

    event_type = event['type']
    event_handler = event_map.get(event_type, handler.handle_event)

    response = event_handler(event)
    return response
