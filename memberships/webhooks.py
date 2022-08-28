
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe
#from memberships.webhook_handler import Stripe_Webhook_Handler


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
        
    print(event)
    return HttpResponse(content="SUCCESS!!", status=200)

    # Handle the checkout.session.completed event
    # if event['type'] == 'checkout.session.completed':
    #     session = event['data']['object']
    #     try:
    #         current_profile = get_object_or_404(Profile, user=request.user)
    #         stripe.api_key = settings.STRIPE_SECRET_KEY
    #     except Exception as e:
    #         return JsonResponse({'error': (e.args[0])}, status=403)
    #         print(e)

    #     # Fetch all the required data from session
    #     session = stripe.checkout.Session.retrieve(request.GET.get('session_id'))
    #     customer = stripe.Customer.retrieve(session.customer)
    #     subscription = stripe.Subscription.retrieve(session.subscription)
    #     current_profile.is_subscribed = True
    #     current_profile.stripe_customer_id = customer.id
    #     current_profile.stripe_subscription_id = subscription.id
    #     try:
    #         current_profile.save()
    #     except Exception as e:
    #         print(e)
    #         return JsonResponse({'error': (e.args[0])}, status=403)
    #     print(current_profile.user + ' just subscribed.')
