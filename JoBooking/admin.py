from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Offre, Commande, Reservation


# ici formulaire connexion pour acces à l'administration
class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(label='email')
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email']

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# l'ajout de ModelADmin permet la personnalisation de l'affichage sur l'interface
class AdminInterface(BaseUserAdmin):
    login_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'checked_email', 'cle_inscription',)


class AdminOffre(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'billet', 'ventes')


class AdminCommande(admin.ModelAdmin):
    list_display = ('user', 'offre_id', 'quantity', 'paiement', 'cle_paiement', 'date_commande')


class AdminReservation(admin.ModelAdmin):
    list_display = ('user', 'commandes_list')


admin.site.register(CustomUser, AdminInterface, )
admin.site.register(Offre, AdminOffre)
admin.site.register(Commande, AdminCommande)
admin.site.register(Reservation, AdminReservation)

# modification interface admin
admin.site.site_title = 'Jeux olympiques Gestion'
admin.site.site_header = 'Jeux olympiques Gestion'
admin.site.index_title = 'Jeux olympiques Gestion'
