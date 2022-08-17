from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Activity

# Create your views here.
# def user_profile_check(user):
#     """
#     Checks if a profile is associated with this user
#     """
#     if user.is_authenticated:
#         current_profile = get_object_or_404(Profile, user=user)
#         if current_profile.membership:
#             existing_user = True
#     else:
#         existing_user = True
#     return existing_user


def all_activities(request):
    """A view to show all activities"""

    activity_list = get_list_or_404(Activity)

    context = {'activity_list': activity_list}

    return render(request, 'activities/all_activities.html', context)


def activity_page(request, key):
    """ A view to return the activity page """

    current_activity = get_object_or_404(Activity, pk=key)

    context = {'current_activity': current_activity}
    return render(request, 'activities/activity_page.html', context)
