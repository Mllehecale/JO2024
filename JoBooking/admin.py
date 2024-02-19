from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


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


class AdminInterface(BaseUserAdmin):
    login_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')


admin.site.register(CustomUser, AdminInterface)
