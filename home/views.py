from django.shortcuts import render

def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def club(request):
    """ A view to return the index page """

    return render(request, 'club.html')