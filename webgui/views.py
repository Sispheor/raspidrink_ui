from django.shortcuts import render
from models import Bottle, Cocktail, Cocktailinfo


def homepage(request):
    """
    Homepage of the Bar Pi app. Show all availlable coktail
    :param request: metadata about the request
    :return: Homepage
    """

    cocktails = Cocktail.objects.all()
    return render(request, 'homepage.html', {'coktails': cocktails})
