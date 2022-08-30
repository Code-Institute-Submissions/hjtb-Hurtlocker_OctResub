from django.conf import settings
from django.http import JsonResponse, HttpResponse
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
        print(e)        
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        return HttpResponse(status=400)

    except Exception as e:
        print(e)
        return JsonResponse({'error': (e.args[0])}, status=403)

    handler = Stripe_Webhook_Handler(request)

    event_map = {
        'checkout.session.completed': handler.handle_checkout_complete,
        'customer.subscription.deleted': handler.handle_subscription_deleted,
        'invoice.payment_succeeded': handler.handle_payment_succeeded,
        'invoice.payment_failed': handler.handle_payment_failed,
    }

    event_type = event['type']
    event_handler = event_map.get(event_type, handler.handle_event)

    response = event_handler(event)
    return response
