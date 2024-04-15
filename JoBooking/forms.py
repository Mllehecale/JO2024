from django import forms

""" formaulaire pour la connexion"""


class Connexion(forms.Form):
    email = forms.EmailField(label='', widget = forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'Mot de Passe'}))
