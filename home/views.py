from django.shortcuts import render

def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def club(request):
    """ A view to return the club page """

    return render(request, 'club.html')


def activity(request):
    """ A view to return the activity page """

    return render(request, 'activity.html')


def profile(request):
    """ A view to return the profile page """

    return render(request, 'profile.html')


def login(request):
    """ A view to return the login page """

    return render(request, 'login.html')


def register(request):
    """ A view to return the register page """

    return render(request, 'register.html')