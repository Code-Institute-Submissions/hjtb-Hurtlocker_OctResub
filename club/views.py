from django.shortcuts import render, get_list_or_404
from activities.models import Activity
from memberships.models import Membership
from profiles.models import Profile

# Create your views here.


def club_page(request):
    """ A view to return the club page """

    activity_list = get_list_or_404(Activity)
    membership_list = get_list_or_404(Membership)
    profile_list = get_list_or_404(Profile)

    context = {'activity_list': activity_list,
               'membership_list': membership_list,
               'profile_list': profile_list
               }

    return render(request, 'club/club_page.html', context)
