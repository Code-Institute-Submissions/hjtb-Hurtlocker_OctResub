from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse

from activities.models import Activity
from profiles.models import Profile
from .models import Membership
from .forms import SignupForm


# Create your views here.


def all_memberships(request):
    """
    A view to show all memberships
    """

    memberships_list = get_list_or_404(Membership)

    context = {'memberships_list': memberships_list}

    return render(request, 'memberships/all_memberships.html', context)


def membership_page(request, key):
    """
    A view to return the membership page
    """

    current_membership = get_object_or_404(Membership, pk=key)

    activities_list = get_list_or_404(Activity)

    context = {
        'current_membership': current_membership,
        'activities_list': activities_list,
    }
    return render(request, 'memberships/membership_page.html', context)


def membership_signup(request):
    """
    Get information from the user before they pay
    """

    current_profile = get_object_or_404(Profile, user=request.user)
    memberships_list = get_list_or_404(Membership)

    if request.method == 'POST':
        form = SignupForm(request.POST, instance=current_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has signed up')
            return redirect('/')
        else:
            messages.error(request, 'Please ensure the data entered is valid.')

    else:
        form = SignupForm(instance=current_profile)

    context = {
        'form': form,
        'memberships_list': memberships_list,
    }
    return render(request, 'memberships/membership_signup.html', context)
