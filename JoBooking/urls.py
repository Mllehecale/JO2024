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
    path("reservation/", views.reservation, name="reservation"),
    path("reservation/annulation", views.annulation, name="annulation"),
    path("reservation/paiement/payer", views.payer, name="payer"),
    path("reservation/paiement", views.paiement, name="paiement"),
    path("reservation/remerciements", views.remerciements, name="remerciements"),

]
