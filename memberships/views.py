from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
import os
from datetime import datetime as dt

from profiles.models import Profile
from .forms import SignupForm


@login_required
def membership_signup(request):
    """
    Get information from the user before they pay
    """

    current_profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES, instance=current_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has signed up')
            return redirect('/memberships/checkout')
        else:
            messages.error(
                request, 'Please ensure the data entered is valid.')
    else:
        form = SignupForm(
            instance=current_profile,
            initial={
                'email': request.user.email,
            },
            )

    context = {
        'form': form,
    }
    return render(request, 'memberships/membership_signup.html', context)


@login_required
def checkout(request):
    """
    A view to allow users to checkout
    """

    current_profile = get_object_or_404(Profile, user=request.user)

    if current_profile.is_subscribed or not (
        current_profile.first_name and current_profile.last_name
            ):
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
    if os.environ.get('GITPOD_WORKSPACE_ID'):
        domain_url = 'http://8000-hjtb-hurtlocker-n667ue81604.ws-eu63.gitpod.io/'
    else:
        domain_url = 'https://hurtlocker-jtb.herokuapp.com/'
        
    try:
        current_profile = get_object_or_404(Profile, user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        existing_customers = stripe.Customer.list()
        # for customer in existing_customers:
        #     print(customer)
        #     if current_profile.email == customer.email:
        #         current_profile.stripe_customer_id = customer.id
        #     print(current_profile.email)
        if current_profile.stripe_customer_id:
            customer_id = current_profile.stripe_customer_id
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.current_profile.id,
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
        customer_id = stripe.Customer.retrieve(session.customer).id
        subscription_id = stripe.Subscription.retrieve(session.subscription).id
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


@login_required
def subscription_cancelled(request):
    """
    A view to show member they've cancelled their membership
    """

    try:
        current_profile = get_object_or_404(Profile, user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(request.GET.get('session_id'))
        customer_id = stripe.Customer.retrieve(session.customer).id
        subscription_id = stripe.Subscription.retrieve(session.subscription).id
        subscription_end = dt.fromtimestamp(current_profile.subscription_end)
    except Exception as e:
        print(e)
        return JsonResponse({'error': (e.args[0])}, status=403)

    context = {
        'session': session,
        'customer': customer_id,
        'current_profile': current_profile,
        'subscription': subscription_id,
        'subscription_end': subscription_end,
    }
    return render(request, 'memberships/subscription_cancelled.html', context)
