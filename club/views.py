from django.shortcuts import render
# from activities.models import Activity
# from memberships.models import Membership
# from profiles.models import Profile

# Create your views here.


def club_page(request):
    """ A view to return the club page """

    return render(request, 'club/club_page.html', context)
