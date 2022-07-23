from django.shortcuts import render
from .models import Profile

# Create your views here.


def all_profiles(request):
    """A view to show all profiles"""

    # profile_list = Profile.objects.all()

    profile_list = [
        {'id': 1, 'name': 'Tom'},
        {'id': 2, 'name': 'Jane'},
        {'id': 3, 'name': 'Sarah'},
        {'id': 4, 'name': 'Jim'},
    ]
    context = {'profile_list': profile_list}

    return render(request, 'profiles/all_profiles.html', context)


def profile_page(request, key):
    """ A view to return the profile page """

    current_profile = None

    # profile_list = Profile.objects.all()

    profile_list = [
        {'id': 1, 'name': 'Tom'},
        {'id': 2, 'name': 'Jane'},
        {'id': 3, 'name': 'Sarah'},
        {'id': 4, 'name': 'Jim'},
    ]

    for profile_item in profile_list:
        # When using db change this to dot notation
        if profile_item['id'] == int(key):
            current_profile = profile_item
    context = {'current_profile': current_profile}
    return render(request, 'profiles/profile_page.html', context)
