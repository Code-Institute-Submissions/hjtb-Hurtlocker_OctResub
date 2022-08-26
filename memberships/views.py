from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

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
        if current_profile.is_subscribed:
            existing_user = True
    else:
        existing_user = True
    return existing_user


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
        'stripe_public_key': 'pk_test_51LUx5ZHw2Z3gzQYHe5Ys0QQKavkVo0tb9d7tphwAZmqEwN69LGV8YXhqenqOHeJv2JTOeD274sYSEGc37IXtr2SH00KHTpeI4p',
        'client_secret': 'test_client_secret',
    }
    return render(request, 'memberships/membership_signup.html', context)


def checkout(request):
    """
    A view to allow users to checkout
    """

    if request.user.is_authenticated:
        try:
            current_profile = get_object_or_404(Profile, user=request.user)
        except Exception as e:
            print(e)
            return JsonResponse({'error': (e.args[0])}, status=403)
    else:
        return redirect('/account/login')

    context = {
        'current_profile': current_profile,
        'stripe_public_key': 'pk_test_51LUx5ZHw2Z3gzQYHe5Ys0QQKavkVo0tb9d7tphwAZmqEwN69LGV8YXhqenqOHeJv2JTOeD274sYSEGc37IXtr2SH00KHTpeI4p',
        'client_secret': 'test_client_secret',
    }
    return render(request, 'memberships/checkout.html', context)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)
