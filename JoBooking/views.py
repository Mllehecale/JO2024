from django.shortcuts import render, redirect
from django.contrib.auth import login
from .authentification import CustomAuthentification
from .forms import Connexion
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'JoBooking/index.html')


def offres(request):
    return render(request, 'JoBooking/offres.html')


def inscription(request):
    form = UserCreationForm()
    return render(request, 'JoBooking/inscription.html',context={'form':form})


def connexion(request):
    message = ""
    if request.method == 'POST':
        form = Connexion(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            custom_auth = CustomAuthentification()
            user = custom_auth.authenticate(request, email=email, password=password)

            # email = request.POST.get('email')
            # password = request.POST.get('password')

            if user is not None:
                login(request, user)
                message = f'Bienvenue {user.name} ! Vous êtes connecté.'
                return redirect('index.html')
            else:
                message = 'Identifiants non valides.'
                return render(request, 'connexion.html')
    else:
        form = Connexion()

    return render(request, 'connexion.html', context={'form': form, 'message': message})
