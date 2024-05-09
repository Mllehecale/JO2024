import io
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import Connexion
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Offre, Reservation, Commande
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import activation_compte
from django.core.mail import EmailMessage
from django.contrib import messages
from .authbackends import EmailAuthBackend
from django.contrib.auth.decorators import login_required
import uuid
import json
from fpdf import FPDF
from PyPDF2 import PdfMerger, PdfReader
from io import BytesIO
from django.http import HttpResponse
import qrcode
import boto3
from botocore.client import Config


# méthode pour créer un formulaire d'inscription (utilisation du formulaire émit par django par défaut)
class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser  # ici on spécifie qu'on veut ce modèle personnalisé
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['email'].label = ''

        self.fields['email'].required = True
        self.fields['email'].widget.attrs['placeholder'] = 'adresse@mail.com'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nom'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Prénom'
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['password1'].widget.attrs['placeholder'] = 'Mot de passe'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmation Mot de passe'
        self.fields['password1'].help_text = '<br>Minimum 8 caractères - Pas de mot de passe tout en numérique'
        self.fields['password2'].help_text = '<br>Saisir le mot de passe de nouveau'


# view pour la page d'accueil
def index(request):
    return render(request, 'JoBooking/index.html')


# view pour la page des offres
def offres(request):
    list_offres = Offre.objects.all().order_by('id')  # affiche toutes les offres  = plan solo,duo,team ou autre
    commandes_user = {}  # creation dictionnaire pour offre deja acheté
    if request.user.is_authenticated:
        commandes_utilisateur = Commande.objects.filter(user=request.user)
        for com in commandes_utilisateur:
            commandes_user[com.offre_id] = True  # recupération de l'id
    context = {'offres': list_offres, 'commandes_user': commandes_user}
    return render(request, 'JoBooking/offres.html', context)


# view pour la page d'inscription
def inscription(request):
    context = {}  # stockage données  lors du rendu de page

    if request.method == 'POST':  # vérification methode de la requête est POST = formulaire soumis
        form = CustomSignupForm(request.POST)  # création formulaire avec données POST
        if form.is_valid():  # vérification  de la validité des données
            user = form.save()  # sauvegarde dans la BDD mais enregistrement pas immediat
            user.cle_inscription = uuid.uuid4().hex  # generation clé d'inscription
            user.save()
            # connexion automatique
            if user is not None:  # signification : si l'user a été trouvée ...
                login(request, user, backend='JoBooking.authbackends.EmailAuthBackend')

                return redirect('verification_email')  # redirection de l'utilisateur vers page verification mail
        else:
            context['errors'] = form.errors  # erreur de validation

    form = CustomSignupForm()  # nouvelle page d'inscription vide  donc sans POST
    context['form'] = form
    return render(request, 'JoBooking/inscription.html', context=context)  # renvoie page d'inscription


# view vérification email
# message pour correcteur : je me suis inspiré car c'est complexe a mettre en place
# https://www.paleblueapps.com/rockandnull/django-email-verification/
def verification_email(request):
    if request.method == "POST":
        if isinstance(request.user, CustomUser) and request.user.checked_email != True:
            user = request.user
            current_site = get_current_site(request)
            email = request.user.email
            subjet = "Vérification de votre email"
            message = render_to_string('message_verification_email.html', {
                'domain': current_site.domain,
                'request': request,
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': activation_compte.make_token(user),

            })
            email = EmailMessage(
                subjet, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            return redirect('email_verifie')
        else:
            messages.warning(request, 'Impossible envoi mail de verification')
    return render(request, 'verification_email.html')


def email_verifie(request):
    return render(request, 'email_verifie.html')


def confirmation_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and activation_compte.check_token(user, token):
        user.checked_email = True
        user.save()
        messages.success(request, 'Votre email a bien été vérifié.')
        return redirect('inscription_reussie')
    else:
        messages.warning(request, 'Le lien est invalide.')
    return render(request, 'verification_email.html')


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
                f'Bienvenue {user.first_name} ! Vous êtes connecté.'
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


#  renvoie  à la page panier
@login_required(login_url='connexion')  # connexion nécessaire pour avoir accès a cette page
def commande(request):
    if request.method == 'POST':
        user = request.user
        panier_data = json.loads(request.body)
        print('données envoyés par front:', panier_data)
        if 'panier' in panier_data:
            for offre_id, offre_data in panier_data['panier'].items():
                offre_id = offre_data['id']
                # offre_quantity = offre_data['quantity']
                com, created = Commande.objects.get_or_create(user=user,
                                                              offre_id=offre_id)  # récupération commande
                if created:  # exemple:  une offre n'est pas dans la commande donc elle sera crée #
                    # else:   l'offre est deja dans la commande donc on augmente la quantité
                    # commande.quantity = offre_quantity
                    com.save()
    # récupération des commandes impayées ( par defaut paimement = False car pas encore payé)
    commandes_impayees = Commande.objects.filter(user=request.user, paiement=False)

    if commandes_impayees:
        return render(request, 'panier.html', context={'commandes_impayees': commandes_impayees})
    else:
        return render(request, 'panier_vide.html')


# methode pour annuler une réservation au complet
def annulation(request):
    commandes_impayees = Commande.objects.filter(user=request.user, paiement=False)
    if commandes_impayees:
        for com in commandes_impayees:
            com.quantity = 0
            com.save()
    commandes_impayees.delete()  # suppression commandes impayés dans le panier.s

    return redirect('index')  # retourne vers la page d'accueil


def supprimer_offre(request):
    if request.method == 'POST':
        user = request.user
        panier_data = json.loads(request.body)
        print('données envoyés par front:', panier_data)
        offre_id = panier_data.get('offre_id')
        Commande.objects.filter(user=user, offre_id=offre_id).delete()
        print('offre supprimé du panier')

    return redirect('commande')


def remerciements(request):
    return render(request, 'remerciements.html')


def payer(request):
    user = request.user
    commandes_impayees = Commande.objects.filter(user=user, paiement=False)

    for com in commandes_impayees:
        offre = com.offre  # récupration du plan dans la commande
        com.paiement = True  # les commandes sont payés
        com.save()
        if com.paiement is True:
            cle_paiement = uuid.uuid4().hex
            com.cle_paiement = cle_paiement
            com.save()

            offre.ventes += com.quantity  # si paiement =True  ça augmente ventes de l'offre
            offre.save()

    return render(request, 'remerciements.html')


def telechargement_pdf(request):
    if isinstance(request.user, CustomUser):
        user = request.user
        pdf_commandes = []
        filename = "BilletsJo.pdf"
        commandes_payees = Commande.objects.filter(user=user, paiement=True)

        for com in commandes_payees:
            offre = com.offre  # récupration du plan dans la commande
            date = com.date_commande
            pdf_telechageable = creation_billet(user, offre, date)
            pdf_content_str = pdf_telechageable.output(dest='S').encode('latin1')  # a faire selon la doc fpdf
            pdf_commandes.append(pdf_content_str)
        pdf_fusion = fusion_pdf(pdf_commandes, filename)  # redirige user vers page de remerciements si pdf
        return pdf_fusion


def paiement(request):
    total = 0  # mise en place logique calcul total du panier
    user = request.user
    commandes_impayees = Commande.objects.filter(user=user, paiement=False)
    if commandes_impayees:
        for com in commandes_impayees:
            total += com.offre.price
    return render(request, 'paiement.html', context={'commandes_impayees': commandes_impayees, 'total': total})


# création d'un pdf contenant billet (selon nb de billet de offre)
def creation_billet(user, offre, date):
    pdfs = []
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    # cle_unique = ""
    # un user peut avoir plusieurs commandes donc plusieurs clés de paiements
    # creation qr code + concaténation : clé inscription et clé paiment,  unique à chaque user
    commandes_payees = Commande.objects.filter(user=user, paiement=True)
    for com in commandes_payees:
        # permet affichage des cles de paiement  et plans choisi par l'user sur scan qrcode
        commandes_str = '|'.join([str(com.offre) for com in commandes_payees])
        cles_paiement = '|'.join([str(com.cle_paiement) for com in commandes_payees])
        user_name = f"{user.last_name} {user.first_name}" if user.first_name and user.last_name else ""
        cle_unique = f"clé inscription:{user.cle_inscription}" \
                     f"|clés paiement:{cles_paiement}|titulaire:{user_name}" \
                     f"|plan(s):{commandes_str}"
        # creation du qrcode
        qr = qrcode.make(cle_unique)
        qr_path = "qr_code.png"
        qr.save(qr_path)
        # dynamisation position y pour qr code but: eviter qu'ils se superposent si plusieurs billets
        espace_y = 55
        position_y = 35
        # ajout logo sur billet

        # un pdf contient nb de billet selon offre
        for b in range(offre.billet):
            pdf.cell(0, 10, "_______________________________________________________________________________", ln=True,
                     align="LEFT")
            pdf.cell(0, 10, "   BILLET(S) POUR LES JEUX OLYMPIQUES FRANCE 2024 ", ln=True, align="CENTER")
            pdf.cell(0, 5, "_______________________________________________________________________________", ln=True,
                     align="LEFT")
            pdf.cell(0, 10, f'Titulaire du billet: {user.last_name} {user.first_name}', ln=True, align="LEFT")
            pdf.cell(0, 10, f'Plan: {offre}', ln=True, align="LEFT")
            pdf.cell(0, 10, f'Date & Heure réservation:{date}', ln=True, align="LEFT")

            y = position_y + b * espace_y  # calcul pour dynamiser la position de y
            pdf.image(qr_path, x=170, y=y, w=30, h=30)

        # user_name = f"{user.last_name}{user.first_name}" if user.first_name and user.last_name else ""
        # pdf_output_file = f"billet_{offre.title}_{user_name}.pdf"
        # pdf.output(pdf_output_file)

        pdfs.append(pdf)
        print(" pdf vue creation:", len(pdfs))  # doit avoir un seul pdf
        return pdf


#  code pour fusionner pdf si plusieurs commandes
def fusion_pdf(pdf_contents, filename):
    merger = PdfMerger()
    output = BytesIO()

    for pdf_content in pdf_contents:
        reader = PdfReader(BytesIO(pdf_content))
        merger.append(reader)

    merger.write(output)
    merger.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(output.getvalue())
    return response


@login_required(login_url='connexion')  # connexion nécessaire pour avoir accès  page reservation
def reservation(request):
    if isinstance(request.user, CustomUser):
        reservation_user, created = Reservation.objects.get_or_create(user=request.user)
        commandes_payees = Commande.objects.filter(user=request.user, paiement=True)

        user = request.user
        pdf_url = None
        if created:
            reservation_user.commandes.set(commandes_payees)
            reservation_user.save()
        else:
            for com in commandes_payees:
                if com.billet_pdf:
                    pdf_url = com.billet_pdf
                else:
                    user = request.user
                    offre = com.offre  # récupration du plan dans la commande
                    date = com.date_commande
                    pdf_telechageable = creation_billet(user, offre, date)
                    pdf_content = pdf_telechageable.output(dest='S').encode('latin1')
                    print('contenu:', len(pdf_content))
                    file_name = f"billet_{com.offre.title}_{user.last_name}{user.first_name}.pdf"

                    # operation qui permet de telecharger PDF via le bucket  sur s3
                    # ajouter s3v4 car sinon pdf inacessible via bucket
                    s3_client = boto3.client('s3', region_name='eu-west-3', config=Config(signature_version='s3v4'))
                    bucket_name = 'bucketjofrancehecale'
                    key = file_name
                    expiration = 3600  # pour ce projet  on definit une expiration d'1h
                    pdf_url = s3_client.generate_presigned_url('get_object',
                                                               Params={'Bucket': bucket_name, 'Key': key},
                                                               ExpiresIn=expiration,
                                                               HttpMethod='GET'
                                                               )
                    com.billet_pdf = pdf_url
                    com.save()
                    # operation qui permet de stocker le pdf dans le bucket sur S3
                    with io.BytesIO(pdf_content) as f:
                        s3_client.upload_fileobj(f, bucket_name, key, ExtraArgs={'ContentType': 'application/pdf'})

                if com not in reservation_user.commandes.all():
                    reservation_user.commandes.add(com)
            reservation_user.save()

        return render(request, 'reservation.html',
                      context={'commandes_payees': commandes_payees, 'pdf_url': pdf_url})


def jeux(request):
    return render(request, 'jeux.html')


def panier_vide(request):
    return render(request, 'Panier_vide.html')
