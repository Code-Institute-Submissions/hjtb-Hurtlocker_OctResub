from django.shortcuts import render, get_object_or_404
from .models import Profile

# Create your views here.


def all_profiles(request):
    """A view to show all profiles"""

    profile_list = Profile.objects.all()

    context = {'profile_list': profile_list}

    return render(request, 'profiles/all_profiles.html', context)


def profile_page(request, key):
    """A view to return the individual profile page"""

    current_profile = get_object_or_404(Profile, pk=key)

    context = {'current_profile': current_profile}
    return render(request, 'profiles/profile_page.html', context)
