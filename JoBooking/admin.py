from django.contrib import admin
from .forms import ConnexionAdmin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class AdminInterface(UserAdmin):
    login_form = ConnexionAdmin
    list_display = ('email', 'username', 'last_name', 'is_staff')


admin.site.register(CustomUser, AdminInterface)
