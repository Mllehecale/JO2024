from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("offres/", views.offres, name="offres"),
    path("inscription/", views.inscription, name="inscription"),
    path("connexion/", views.connexion, name="connexion"),
    path("deconnexion/", views.deconnexion, name="deconnexion"),
    path("inscription_réussie/", views.inscription_reussie, name="inscription_reussie"),
    path("commande/", views.commande, name="commande"),
    path("commande/annulation", views.annulation, name="annulation"),
    path("commande/payer", views.payer, name="payer"),
    path("commande/paiement", views.paiement, name="paiement"),
    path("remerciements/", views.remerciements, name="remerciements"),

]
