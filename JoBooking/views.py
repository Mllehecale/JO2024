from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import Connexion
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Offre, Reservation, Commande
from .authbackends import EmailAuthBackend
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import uuid


# méthode pour créer un formulaire d'inscription (utilisation du formulaire émit par django par défaut)
class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser  # ici on spécifie qu'on veut ce modèle personnalisé
        fields = ('first_name', 'last_name', 'email')


# view pour la page d'accueil
def index(request):
    return render(request, 'JoBooking/index.html')


# view pour la page des offres
def offres(request):
    list_offres = Offre.objects.all()  # affiche toutes les offres  = plan solo,duo,family ou autre
    context = {'offres': list_offres}
    return render(request, 'JoBooking/offres.html', context)


# view pour la page d'inscription
def inscription(request):
    context = {}  # stockage données  lors du rendu de page

    if request.method == 'POST':  # vérification methode de la requête est POST = formulaire soumis
        form = CustomSignupForm(request.POST)  # création formulaire avec données POST
        if form.is_valid():  # vérification  de la validité des données
            user = form.save()  # sauvegarde dans la BDD
            user.cle_inscription = uuid.uuid4().hex
            user.save()

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
                return render(request, 'connexion.html',
                              context={'message': message})  # user non trouvé, donc retourne page connexion
    else:
        form = Connexion()

    return render(request, 'connexion.html', context={'form': form, 'message': message})


# méthode pour que les users se déconnecte
def deconnexion(request):
    logout(request)
    return redirect('index')


# méthode pour ajouter à réservation. ( réservation c'est le panier. J'ai volontairement choisi ce terme)
def ajouter_reservation(request, offre_id):
    user = request.user
    offre = get_object_or_404(Offre, id=offre_id)  # ici on récupère l'offre si inexistante,erreur 404
    reservation, _ = Reservation.objects.get_or_create(user=user)  # récupération du panier
    commande, created = Commande.objects.get_or_create(user=user,
                                                       offre=offre)  # récupération commande

    if created:  # exemple:  une offre n'est pas dans la commande donc elle sera crée
        reservation.commandes.add(commande)
        reservation.save()
    else:  # l'offre est deja dans la commande donc on augmente la quantité
        commande.quantity += 1
        commande.save()
    return redirect('offres')


#  renvoie  à la page de reservation (c'est la page panier, après avoir réserver)
@login_required(login_url='connexion')  # connexion nécessaire pour avoir accès a cette page
def reservation(request):
    reservation = get_object_or_404(Reservation, user=request.user)
    return render(request, 'reservation.html', context={
        'commandes': reservation.commandes.all()})  # affiche tous les éléments qu'ya dans la réservation


# methode pour annuler une réservation au complet
def annulation(request):
    user_reservation = Reservation.objects.get(user=request.user)
    if user_reservation:  # si elle existe
        user_reservation.commandes.all().delete()
        user_reservation.delete()  # suppression de tout ce qu'y a dans la réservation qu'on supprime ensuite

    return redirect('index')  # retourne vers la page d'accueil


def payer(request):
    reservation = request.user.reservation

    # génération de billets (combinaison des deux clés générées , qr code, nom acheteur + logo ;date de l'evement )

    # augmentation de ventes de Offre selon la quantité achetée
    for commande in reservation.commandes.all():
        offre = commande.offre  # récupration du plan dans la commande
        offre.ventes += commande.quantity
        offre.save()
    # paiement dans Reservation devient TRUE (initialement à FALSE)
    reservation.paiement = True
    reservation.save()

    # génération de clé unique pour paiment seulement si payer.
    if reservation.paiement == True:
        cle_paiement = uuid.uuid4().hex
        reservation.cle_paiement = cle_paiement
        reservation.save()

    # le panier (réservation ) est réinitialisé
    reservation.commandes.clear()
    # Renvoie à la page de remerciement où on peut telecharger billet
    return redirect('remerciements')


def remerciements(request):
    return render(request, 'remerciements.html')
