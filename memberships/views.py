from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
from datetime import datetime

from profiles.models import Profile
from .forms import SignupForm


def user_profile_check(user):
    """
    Checks if a profile is associated with the user
    """
    
    now = datetime.now()
    current_time = datetime.timestamp(now)
    user_has_profile = False
    if user.is_authenticated:
        try:
            current_profile = get_object_or_404(Profile, user=user)
            if current_profile.subscription_end:
                if current_profile.subscription_end <= current_time:
                    current_profile.is_subscribed = False
            else:
                pass
        except ObjectDoesNotExist:
            current_profile = None

        if current_profile.first_name and current_profile.last_name:
            user_has_profile = True
    else:
        user_has_profile = True
    return user_has_profile


@login_required
def membership_signup(request):
    """
    Get information from the user before they pay
    """
    try:
        current_profile = get_object_or_404(Profile, user=request.user)
        current_profile.email = request.user.email
        form = SignupForm(request.POST, instance=current_profile)
    except Exception as e:
        print(e)
        return JsonResponse({'error': (e.args[0])}, status=403)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'User has signed up')
            return redirect('/memberships/checkout')
        else:
            messages.error(
                request, 'Please ensure the data entered is valid.')

    context = {
        'form': form,
    }
    return render(request, 'memberships/membership_signup.html', context)


@login_required
def checkout(request):
    """
    A view to allow users to checkout
    """
    try:
        current_profile = get_object_or_404(Profile, user=request.user)
        if current_profile.stripe_customer_id:
            customer_id = current_profile.stripe_customer_id
    except Exception as e:
        return JsonResponse({'error': (e.args[0])}, status=403)

    if current_profile.is_subscribed:
        return redirect('/club')
    else:
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe.api_key = settings.STRIPE_SECRET_KEY
        price_id = settings.STRIPE_PRICE_ID
        price_object = stripe.Price.retrieve(price_id,)
        price = f'€{"%0.2f" % int(price_object.unit_amount/100)}'
        subscription_details = stripe.Product.retrieve(
            price_object.product
            ).description
        billing_name = f"{current_profile.first_name} {current_profile.last_name}"
        billing_email = current_profile.email

    context = {
        'current_profile': current_profile,
        'stripe_public_key': stripe_public_key,
        'price': price,
        'customer_id': customer_id,
        'billing_name': billing_name,
        'billing_email': billing_email,
        'client_secret': 'test_client_secret',
        'subscription_details': subscription_details,
    }
    return render(request, 'memberships/checkout.html', context)


@csrf_exempt
@login_required
def create_checkout_session(request):
    """
    A view to create a stripe checkout session
    """

    try:
        current_profile = get_object_or_404(Profile, user=request.user)
        domain_url = 'http://8000-hjtb-hurtlockerv1-zs2xiyzn5y4.ws-eu63.gitpod.io/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        existing_customers = stripe.Customer.list()
        if current_profile.email in existing_customers:
            print(current_profile.email)
        if current_profile.stripe_customer_id:
            customer_id = current_profile.stripe_customer_id
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id,
                customer=customer_id,
                success_url=domain_url + 'memberships/checkout_success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'club/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
        else:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id,
                customer_email=current_profile.email,
                success_url=domain_url + 'memberships/checkout_success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'club/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(e)
        return JsonResponse({'error': (e.args[0])}, status=403)


@login_required
def checkout_success(request):
    """
    A view to process a successful checkout
    """

    try:
        current_profile = get_object_or_404(Profile, user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(request.GET.get('session_id'))
        customer_id  = stripe.Customer.retrieve(session.customer).id
        subscription_id  = stripe.Subscription.retrieve(session.subscription).id
    except Exception as e:
        print(e)
        return JsonResponse({'error': (e.args[0])}, status=403)

    context = {
        'session': session,
        'customer': customer_id,
        'current_profile': current_profile,
        'subscription': subscription_id,
    }
    return render(request, 'memberships/checkout_success.html', context)
