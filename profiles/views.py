from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm

# Create your views here.


def all_profiles(request):
    """A view to show all profiles"""

    profile_list = get_list_or_404(Profile)

    context = {'profile_list': profile_list}

    return render(request, 'profiles/all_profiles.html', context)


def profile_page(request, key):
    """A view to return the individual profile page"""

    current_profile = get_object_or_404(Profile, pk=key)
    member_activity_list = current_profile.activities.all()

    form = ProfileForm(instance=current_profile)

    context = {
        'form': form,
        'current_profile': current_profile,
        'member_activity_list': member_activity_list,
        }
    return render(request, 'profiles/profile_page.html', context)


def edit_profile(request, key):
    """A view to return the individual profile page"""

    current_profile = get_object_or_404(Profile, pk=key)
    member_activity_list = current_profile.activities.all()

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=current_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been updated successfully')
            return redirect('profile_page', key)


    form = ProfileForm(instance=current_profile)

    context = {
        'form': form,
        'current_profile': current_profile,
        'member_activity_list': member_activity_list,
        }
    return render(request, 'profiles/edit_profile.html', context)
