from django.shortcuts import render, redirect
from django.contrib.auth import login
from .authentification import CustomAuthentification
from .forms import Connexion
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser  # ici on spécifie qu'on veut ce modèle personnalisé
        fields = ('last_name', 'first_name', 'email',)


def index(request):
    return render(request, 'JoBooking/index.html')


def offres(request):
    return render(request, 'JoBooking/offres.html')


def inscription(request):
    context = {}  # stockage données  lors du rendu de page

    if request.method == 'POST':  # vérification methode de la requête est POST = formulaire soumis
        form = CustomSignupForm(request.POST)  # création formulaire avec données POST
        if form.is_valid():  # vérification  de la validité des données
            form.save()  # sauvegarde dans la BDD
            return redirect('inscription_reussie')  # redirection de l'utilisateur vers une autre page
        else:
            context['errors'] = form.errors  # erreur de validation

    form = CustomSignupForm()  # nouvelle page d'inscription vide  donc sans POST
    context['form'] = form
    return render(request, 'JoBooking/inscription.html', context=context)  # renvoie page d'inscription


def inscription_reussie(request):
    return render(request, 'inscription_reussie.html')


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
