from django import forms


class Connexion(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
