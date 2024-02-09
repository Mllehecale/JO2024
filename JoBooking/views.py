from django.shortcuts import render, redirect
from django.http import HttpResponse
from .authentification import CustomAuthentification


def index(request):
    return render(request, 'JoBooking/index.html')


def offres(request):
    return render(request, 'JoBooking/offres.html')


def inscription(request):
    return render(request, 'JoBooking/inscription.html')


def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        custom_auth = CustomAuthentification()
        user = custom_auth.authenticate(request,email=email,password=password)

        if user is not None:
            return redirect('JoBooking.index.html')
        else:
            print("Email ou mot de passe invalide")
            return render(request, 'JoBooking.connexion.html')


    else:
        return render(request, 'JoBooking.connexion.html')