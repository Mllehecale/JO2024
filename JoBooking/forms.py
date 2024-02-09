from django import forms


class Connexion(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password', widget=forms.PasswordInput)


class ConnexionAdmin(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password', widget=forms.PasswordInput)
