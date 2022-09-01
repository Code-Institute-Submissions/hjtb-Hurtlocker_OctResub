from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile
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

    # try:
    #     bookings = current_profile.bookings
    # except:
    #     bookings =[]

    context = {
        'current_profile': current_profile,
        # 'bookings': bookings,
        }
    return render(request, 'profiles/profile_page.html', context)


@user_passes_test(user_profile_check, login_url='../memberships/membership_signup')
@login_required
def edit_profile(request, key):
    """A view to edit member profiles"""

    current_profile = get_object_or_404(Profile, pk=key)
    current_user = get_object_or_404(User, email=current_profile.email)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=current_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been updated successfully')
            return redirect('profile_page', key)

    else:
        form = ProfileForm(instance=current_profile)

    context = {
        'form': form,
        'current_profile': current_profile,
        'current_user': current_user,
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
