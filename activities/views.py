from django.shortcuts import render
from .models import Activity

# Create your views here.


def all_activities(request):
    """A view to show all activities"""

    # activity_list = Activity.objects.all()
    activity_list = [
        {'id': 1, 'name': 'rugby'},
        {'id': 2, 'name': 'football'},
        {'id': 3, 'name': 'soccer'},
        {'id': 4, 'name': 'hurling'},
    ]

    context = {'activity_list': activity_list}

    return render(request, 'activities/all_activities.html', context)


def activity_page(request, key):
    """ A view to return the activity page """

    current_activity = None

    # activity_list = Activity.objects.all()

    activity_list = [
        {'id': 1, 'name': 'rugby'},
        {'id': 2, 'name': 'football'},
        {'id': 3, 'name': 'soccer'},
        {'id': 4, 'name': 'hurling'},
    ]

    for activity_item in activity_list:
        # When using db change this to dot notation
        if activity_item['id'] == int(key):
            current_activity = activity_item
    context = {'current_activity': current_activity}
    return render(request, 'activities/activity_page.html', context)
