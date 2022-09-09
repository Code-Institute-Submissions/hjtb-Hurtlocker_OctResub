from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile
from activities.models import Booking, Booking_Slot
from .forms import ProfileForm
import stripe
import os
from datetime import datetime as dt
from django.utils import timezone


def user_subscription_check(user):
    """
    Checks if a member has a subscription
    and if their subscription is in date
    """

    user_is_subscribed = False
    now = dt.now()
    current_time = dt.timestamp(now)

    if not user.is_anonymous:
        current_profile = get_object_or_404(Profile, user=user)
        if current_profile.subscription_end:
            if current_profile.subscription_end <= current_time:
                current_profile.is_subscribed = False
                current_profile.save()
        else:
            pass

        if current_profile.is_subscribed or user.is_staff:
            user_is_subscribed = True

    return user_is_subscribed


def user_is_staff_check(user):
    """
    Checks if a user is staff
    """

    user_is_staff = False
    if user.is_staff:
        user_is_staff = True
        
    return user_is_staff


@login_required
def all_profiles(request):
    """A view to show all profiles"""
    current_profile = get_object_or_404(Profile, user=request.user)

    if not request.user.is_staff:
        messages.error(
            request, 'Only staff can access this page.'
            )
        return redirect('club_page')

    profile_list = get_list_or_404(Profile)

    context = {
        'profile_list': profile_list,
        'current_profile': current_profile
    }

    return render(request, 'profiles/all_profiles.html', context)


@login_required
def profile_page(request, key):
    """A view to return the individual profile page"""

    current_time = timezone.now()
    current_user = request.user

    if key and current_user.is_staff:
        current_profile = get_object_or_404(Profile, pk=key)
    else:
        current_profile = get_object_or_404(Profile, user=request.user)

    try:
        booking_slots = Booking_Slot.objects.all()
    except Booking_Slot.DoesNotExist:
        booking_slots = []

    try:
        members_bookings = Booking.objects.filter(
            member=current_profile, booking_end_time__gte=current_time
            ).order_by('booking_end_time')
    except Booking.DoesNotExist:
        members_bookings = []

    if current_profile.subscription_end:
        subscription_end = dt.fromtimestamp(current_profile.subscription_end)
    else:
        subscription_end = None

    context = {
        'current_profile': current_profile,
        'current_time': current_time,
        'members_bookings': members_bookings,
        'booking_slots': booking_slots,
        'subscription_end': subscription_end,
        'current_user': current_user,
        }
    return render(request, 'profiles/profile_page.html', context)


@user_passes_test(user_subscription_check, login_url='../memberships/membership_signup')
@login_required
def edit_profile(request, key):
    """A view to edit member profile details"""

    current_profile = get_object_or_404(Profile, pk=key)
    profile_user = current_profile.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=current_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been updated successfully')
            return redirect('profile_page', key)
        else:
            messages.error(
                request, 'Please ensure the data entered is valid.'
                )
    else:
        form = ProfileForm(instance=current_profile,
                           initial={
                               'email': profile_user.email
                           },
                           )
    subscription_end = dt.fromtimestamp(current_profile.subscription_end)
    context = {
        'form': form,
        'current_profile': current_profile,
        'subscription_end': subscription_end,
        }
    return render(request, 'profiles/edit_profile.html', context)


@user_passes_test(user_subscription_check, login_url='../memberships/membership_signup')
@login_required
def manage_subscription(request):
    """
    A view to let members access the stript billing portal
    """

    current_profile = get_object_or_404(Profile, user=request.user)
    if current_profile.stripe_customer_id:
        customer_id = current_profile.stripe_customer_id
    else:
        return redirect('profile_page', current_profile.id)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    if os.environ.get('DEVELOPMENT'):
        hostname = os.environ.get('HOSTNAME')
        domain_url = 'https://8000-' + hostname + '.ws-eu64.gitpod.io/'
    else:
        domain_url = 'https://hurtlocker-jtb.herokuapp.com/'
    return_url = domain_url + 'club/'

    try:
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url,
        )
    except Exception as e:
        messages.error(
            request, """
            Sorry, something went wrong when we tried
                to create a session with Stripe, please try again later.
                """
            )
        return HttpResponse(content=e, status=400)

    return redirect(session.url, code=303)


@user_passes_test(user_subscription_check, login_url='../memberships/membership_signup')
@login_required
def cancel_booking(request, key):
    """
    A view to allow members cancel bookings
    """
    current_profile = get_object_or_404(Profile, user=request.user)
    booking_to_be_deleted = get_object_or_404(Booking, pk=key)
    try:
        booking_to_be_deleted.delete()
        messages.success(request, 'Booking Cancelled Successfully')
    except Exception as e:
        messages.error(
            request, """
            Sorry, something went wrong when we tried
                to delete that booking. Please try again later.
                """
            )
        return HttpResponse(content=e, status=400)

    return redirect('profile_page', current_profile.id)
