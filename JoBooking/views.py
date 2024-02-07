from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request,'JoBooking/index.html')


def offres(request):
    return render(request,'JoBooking/offres.html')


def inscription(request):
    return render(request,'JoBooking/inscription.html')


def connexion(request):
    return render(request,'JoBooking/connexion.html')