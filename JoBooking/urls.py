from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("offres/", views.offres, name="offres"),
    path("inscription/", views.inscription, name="inscription"),
    path("connexion/", views.connexion, name="connexion"),
    path("deconnexion/", views.deconnexion, name="deconnexion"),
    path("verification_email/", views.verification_email, name="verification_email"),
    path("email_verifie/", views.email_verifie, name="email_verifie"),
    path("confirmation-email-verifie/<uidb64>/<token>", views.confirmation_email, name="confirmation-email-verifie"),
    path("inscription_réussie/", views.inscription_reussie, name="inscription_reussie"),
    path("commande/", views.commande, name="commande"),
    path("commande/annulation", views.annulation, name="annulation"),
    path("commande/payer", views.payer, name="payer"),
    path("commande/paiement", views.paiement, name="paiement"),
    path("reservation/", views.reservation, name="reservation"),
    path("remerciements/", views.remerciements, name="remerciements"),
    path("telechargement_pdf/", views.telechargement_pdf, name="telechargement_pdf"),
    path("commande/supprimer_offre", views.supprimer_offre, name="supprimer_offre"),
    path("jeux/", views.jeux, name="jeux"),
    path("commande/panier_vide/", views.panier_vide, name="panier_vide"),

]
