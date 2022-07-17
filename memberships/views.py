from django.shortcuts import render
from .models import Membership

# Create your views here.


def all_memberships(request):
    """A view to show all memberships"""

    memberships_list = Membership.objects.all()

    context = {'memberships_list': memberships_list}

    return render(request, 'memberships/all_memberships.html', context)

# individual membership page not working properly
def membership_page(request, key):
    """ A view to return the profile page """

    memberships_list = Membership.objects.all()

    current_membership = None
    for membership_type in memberships_list:
        if membership_type.id == int(key):
            current_membership = membership_type
    context = {'current_membership': current_membership}
    return render(request, 'membership_page.html', context)