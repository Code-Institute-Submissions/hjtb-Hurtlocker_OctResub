from django.shortcuts import render


members = [
    {'member_id': 1, 'member_name': 'john'},
    {'member_id': 2, 'member_name': 'paul'},
    {'member_id': 3, 'member_name': 'jane'},
]


activities = [
    {'activity_id': 1, 'activity_name': 'rugby'},
    {'activity_id': 2, 'activity_name': 'football'},
    {'activity_id': 3, 'activity_name': 'soccer'},
    {'activity_id': 4, 'activity_name': 'hurling'},
]


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def club(request):
    """ A view to return the club page """
    context = {'members': members}
    return render(request, 'club.html', context)


def activities_page(request):
    """ A view to return the activities page """
    context = {'activities': activities}
    return render(request, 'activities_page.html', context)


def activity_page(request, key):
    """ A view to return the selected activity page """
    current_activity = None
    for activity in activities:
        if activity['activity_id'] == int(key):
            current_activity = activity
    context = {'current_activity': current_activity}
    return render(request, 'activity_page.html', context)


def profile(request, key):
    """ A view to return the profile page """
    current_profile = None
    for member in members:
        if member['member_id'] == int(key):
            current_profile = member
    context = {'current_profile': current_profile}
    return render(request, 'profile.html', context)


def login(request):
    """ A view to return the login page """

    return render(request, 'login.html')


def register(request):
    """ A view to return the register page """

    return render(request, 'register.html')
