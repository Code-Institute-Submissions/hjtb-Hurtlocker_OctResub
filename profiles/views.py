from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile
from activities.models import Booking, Booking_Slot
from .forms import ProfileForm
from memberships.views import user_profile_check
# from activities.models import Activity
import stripe

# Create your views here.


@user_passes_test(user_profile_check, login_url='../memberships/membership_signup')
@login_required
def all_profiles(request):
    """A view to show all profiles"""

    if not request.user.is_staff:
# MESSAGE
        return redirect('club_page')

    profile_list = get_list_or_404(Profile)

    context = {'profile_list': profile_list}

    return render(request, 'profiles/all_profiles.html', context)


@user_passes_test(user_profile_check, login_url='../memberships/membership_signup')
@login_required
def profile_page(request, key):
    """A view to return the individual profile page"""

    if key and request.user.is_staff:
        current_profile = get_object_or_404(Profile, pk=key)
    else:
        current_profile = get_object_or_404(Profile, user=request.user)

    try:
        booking_slots = Booking_Slot.objects.all()
    except Booking_Slot.DoesNotExist:
        booking_slots = []

    try:
        members_bookings = Booking.objects.filter(
            member=current_profile
            ).order_by('booking_end_time')
    except Booking.DoesNotExist:
        members_bookings = []

    context = {
        'current_profile': current_profile,
        'members_bookings': members_bookings,
        'booking_slots': booking_slots,
        }
    return render(request, 'profiles/profile_page.html', context)


@user_passes_test(user_profile_check, login_url='../memberships/membership_signup')
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
        form = ProfileForm(instance=current_profile,
            initial={
                'email': profile_user.email
            },
        )

    context = {
        'form': form,
        'current_profile': current_profile,
        }
    return render(request, 'profiles/edit_profile.html', context)


@user_passes_test(user_profile_check, login_url='../memberships/membership_signup')
@login_required
def manage_subscription(request):
    """
    A view to let members access the stript billing portal
    """

    current_profile = get_object_or_404(Profile, user=request.user)
    customer_id = current_profile.stripe_customer_id
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return_url = 'https://8000-hjtb-hurtlockerv1-zs2xiyzn5y4.ws-eu63.gitpod.io/club'

    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )

    return redirect(session.url, code=303)


def cancel_booking(request, key):
    """
    A view to allow members cancel bookings
    """
    current_profile = get_object_or_404(Profile, user=request.user)
    booking_to_be_deleted = get_object_or_404(Booking, pk=key)

    booking_to_be_deleted.delete()
    messages.success(request, 'Booking Cancelled Successfully')

    return redirect('profile_page', current_profile.id)