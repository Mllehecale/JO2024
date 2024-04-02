from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import Connexion
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Offre, Reservation, Commande
from .authbackends import EmailAuthBackend
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import uuid
import json
from fpdf import FPDF
import PyPDF2
from django.http import HttpResponse


# méthode pour créer un formulaire d'inscription (utilisation du formulaire émit par django par défaut)
class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser  # ici on spécifie qu'on veut ce modèle personnalisé
        fields = ('first_name', 'last_name', 'email')

    # a coder soulever erreur si mail non valide(sans@)  ou vide
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True


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
            user.cle_inscription = uuid.uuid4().hex  # generation clé d'inscription
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

            if user is not None:  # signification : si l'user a été trouvée ...
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


#  renvoie  à la page de reservation (c'est la page panier, après avoir réserver)
@login_required(login_url='connexion')  # connexion nécessaire pour avoir accès a cette page
def reservation(request):
    if request.method == 'POST':
        user = request.user
        panier_data = json.loads(request.body)
        print('données envoyés par front:', panier_data)
        if 'panier' in panier_data:
            reservation, _ = Reservation.objects.get_or_create(user=user)  # récupération du panier

            for offre_id, offre_data in panier_data['panier'].items():
                offre_id = offre_data['id']
                # offre_quantity = offre_data['quantity']
                commande, created = Commande.objects.get_or_create(user=user,
                                                                   offre_id=offre_id)  # récupération commande

                if created:  # exemple:  une offre n'est pas dans la commande donc elle sera crée
                    reservation.commandes.add(commande)
                else:  # l'offre est deja dans la commande donc on augmente la quantité
                    # commande.quantity = offre_quantity
                    commande.save()
            reservation.save()
    try:
        reservation = Reservation.objects.get(user=request.user)  # vérification existance réservation
    except Reservation.DoesNotExist:
        return render(request, 'Panier_vide.html')

    return render(request, 'reservation.html', context={
        'commandes': reservation.commandes.all()})  # affiche tous les éléments qu'ya dans la réservation si existe


# methode pour annuler une réservation au complet
def annulation(request):
    user_reservation = Reservation.objects.get(user=request.user)
    if user_reservation:  # si elle existe
        for commande in user_reservation.commandes.all():
            commande.quantity = 0
            commande.save()
        user_reservation.commandes.all().delete()
        user_reservation.delete()  # suppression de tout ce qu'y a dans la réservation qu'on supprime ensuite

    return redirect('index')  # retourne vers la page d'accueil


# création billets  téléchargeables + qr code
def creation_billet(user, offre, date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=12)

    for billet in range(offre.billet):
        pdf.cell(0, 10, text="_______________________________________________________________________________", ln=True, align="LEFT")
        pdf.cell(0, 10, text="   BILLET(S) POUR LES JEUX OLYMPIQUES PARIS 20204 ", ln=True, align="CENTER")
        pdf.cell(0, 5, text="________________________________________________________________________________", ln=True, align="LEFT")

        pdf.cell(0, 10, f'Titulaire du billet: {user.last_name} {user.first_name}', ln=True, align="LEFT")
        pdf.cell(0, 10, f'Plan: {offre}', ln=True, align="LEFT")
        pdf.cell(0, 10, f'Date de réservation:test', ln=True, align="LEFT")

    return pdf


def payer(request):
    reservation = request.user.reservation
    pdf_commandes=[]
    # génération de billets (combinaison des deux clés générées , qr code, nom acheteur + logo ;date de l'evement )
    # augmentation de ventes de Offre selon la quantité achetée
    for commande in reservation.commandes.all():
        offre = commande.offre  # récupration du plan dans la commande
        user = request.user
        #offre = reservation.commandes.first().offre
        date = "date-test"
        pdf_telechageable = creation_billet(user, offre, date)
        pdf_content = pdf_telechageable.output(dest='S').decode('latin1').encode('latin1')
        pdf_commandes.append(pdf_content)

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

    # fusion des PDF  si plusieurs commandes dans la reservation  importation de PyPDF2



    response = HttpResponse(pdf_commandes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="billetJO.pdf"'

    return response

    # le panier (réservation ) est réinitialisé
    reservation.commandes.clear()
    # Renvoie à la page de remerciement où on peut telecharger billet
    return redirect('remerciements')


def remerciements(request):
    return render(request, 'remerciements.html')
