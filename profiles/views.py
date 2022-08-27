from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile
from .forms import ProfileForm
from memberships.views import user_profile_check

# Create your views here.


@user_passes_test(user_profile_check, login_url='../memberships/membership_signup')
@login_required
def all_profiles(request):
    """A view to show all profiles"""

    profile_list = get_list_or_404(Profile)

    context = {'profile_list': profile_list}

    return render(request, 'profiles/all_profiles.html', context)


@user_passes_test(user_profile_check, login_url='../memberships/membership_signup')
@login_required
def profile_page(request, key):
    """A view to return the individual profile page"""

    current_profile = get_object_or_404(Profile, pk=key)

    context = {
        'current_profile': current_profile,
        }
    return render(request, 'profiles/profile_page.html', context)


@user_passes_test(user_profile_check, login_url='../memberships/membership_signup')
@login_required
def edit_profile(request, key):
    """A view to edit member profiles"""

    current_profile = get_object_or_404(Profile, pk=key)

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
        }
    return render(request, 'profiles/edit_profile.html', context)
