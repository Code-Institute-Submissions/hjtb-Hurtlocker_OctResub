from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from activities.models import Activity
from profiles.models import Profile
from memberships.views import user_profile_check
# Create your views here.


@user_passes_test(user_profile_check, login_url='../memberships/membership_signup')
def club_page(request):
    """
    A view to return the club page
    """

    activity_list = get_list_or_404(Activity)
    profile_list = get_list_or_404(Profile)

    context = {'activity_list': activity_list,
               'profile_list': profile_list
               }

    return render(request, 'club/club_page.html', context)
