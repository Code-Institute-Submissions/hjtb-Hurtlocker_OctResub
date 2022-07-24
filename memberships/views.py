from django.shortcuts import render

# Create your views here.


def all_memberships(request):
    """A view to show all memberships"""

    memberships_list = [
        {'id': 1, 'name': 'gold'},
        {'id': 2, 'name': 'silver'},
        {'id': 3, 'name': 'bronze'},
        {'id': 4, 'name': 'platinum'},
    ]

    context = {'memberships_list': memberships_list}

    return render(request, 'memberships/all_memberships.html', context)

# individual membership page not working properly


def membership_page(request, key):
    """ A view to return the profile page """

    memberships_list = [
        {'id': 1, 'name': 'gold'},
        {'id': 2, 'name': 'silver'},
        {'id': 3, 'name': 'bronze'},
        {'id': 4, 'name': 'platinum'},
    ]

    current_membership = None
    for membership_type in memberships_list:
        # When using db change this to dot notation
        if membership_type.id == int(key):
            current_membership = membership_type
    context = {'current_membership': current_membership}
    return render(request, 'memberships/membership_page.html', context)
