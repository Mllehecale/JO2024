from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import Connexion
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .authbackends import EmailAuthBackend


# méthode pour créer un formulaire d'inscription (utilisation du formulaire émit par django par défaut)
class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser  # ici on spécifie qu'on veut ce modèle personnalisé
        fields = ('first_name', 'last_name', 'email',)


# view pour la page d'accueil
def index(request):
    return render(request, 'JoBooking/index.html')


# view pour la page des offres
def offres(request):
    return render(request, 'JoBooking/offres.html')


# view pour la page d'inscription
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


# view pour l'inscripion réussie d'un user
def inscription_reussie(request):
    return render(request, 'inscription_reussie.html')


# view pour la page de connexion
def connexion(request):
    message = ""
    if request.method == 'POST':
        form = Connexion(request.POST)  # création formulaire avec données envoyées via POST
        if form.is_valid():  # vérification de la validité des données
            email = form.cleaned_data['email']  # données nettoyées et récupérées
            password = form.cleaned_data['password']

            custom_auth = EmailAuthBackend()  # implémentation de l'authentification personnalisée
            user = custom_auth.authenticate(request, email=email, password=password)  # appel de la méthode authenticate

            # email = request.POST.get('email')
            # password = request.POST.get('password')

            if user is not None and password is not None:  # signification : si l'user a été trouvée ...
                login(request, user, backend='JoBooking.authbackends.EmailAuthBackend')  # ya 2 backends d'auth
                message = f'Bienvenue {user.first_name} ! Vous êtes connecté.'
                return redirect('/')  # redirige vers la page d'acceuil
            else:
                message = 'Identifiants non valides.'
                return render(request, 'connexion.html')  # user non trouvé, donc retourne page connexion
    else:
        form = Connexion()

    return render(request, 'connexion.html', context={'form': form, 'message': message})
