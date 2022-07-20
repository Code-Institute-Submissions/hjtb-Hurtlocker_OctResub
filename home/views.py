from django.shortcuts import render

# Pipe up the navbar with the various apps and pages

def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def club(request):
    """ A view to return the club page """

    context = {'members': members}
    return render(request, 'club.html', context)




# def login(request):
#     """ A view to return the login page """

#     return render(request, 'login.html')


# def register(request):
#     """ A view to return the register page """

#     return render(request, 'register.html')
