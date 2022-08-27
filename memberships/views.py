from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe

from profiles.models import Profile
from .forms import SignupForm


# Create your views here.
def user_profile_check(user):
    """
    Checks if a profile is associated with the user
    """
    existing_user = False
    if user.is_authenticated:
        try:
            current_profile = get_object_or_404(Profile, user=user)
        except ObjectDoesNotExist:
            pass
        if current_profile.first_name and current_profile.first_name:
            existing_user = True
    else:
        existing_user = True
    return existing_user


@login_required
def membership_signup(request):
    """
    Get information from the user before they pay
    """

    if request.user.is_authenticated:
        try:
            current_profile = get_object_or_404(Profile, user=request.user)
            form = SignupForm(request.POST, instance=current_profile)
        except Exception as e:
            print(e)
            return JsonResponse({'error': (e.args[0])}, status=403)
    else:
        form = SignupForm()

    if request.method == 'POST' and request.user.is_authenticated:
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
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.user.is_authenticated:
        try:
            current_profile = get_object_or_404(Profile, user=request.user)
        except Exception as e:
            print(e)
            return JsonResponse({'error': (e.args[0])}, status=403)
    else:
        return redirect('/accounts/login')

    if current_profile.is_subscribed:
        return redirect('/club')

    else:
        domain_url = 'localhost:8000/'
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY
        stripe.api_key = settings.STRIPE_SECRET_KEY
        price_id = settings.STRIPE_PRICE_ID
        customer_id = current_profile.stripe_customer_id
        billing_name = current_profile.first_name
        billing_email = current_profile.email

    if is_ajax:
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'memberships/signup/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    context = {
        'current_profile': current_profile,
        'stripe_public_key': stripe_public_key,
        'stripe_secret_key': stripe_secret_key,
        'price_id': price_id,
        'customer_id': customer_id,
        'billing_name': billing_name,
        'billing_email': billing_email,
        'client_secret': 'test_client_secret',
    }
    return render(request, 'memberships/checkout.html', context)
