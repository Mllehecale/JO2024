from django.contrib.auth.backends import BaseBackend
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist


class CustomAuthentification(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        user=None
        if email:
            try:
                user = CustomUser.objects.get(email=email)
            except ObjectDoesNotExist:
                return None

            if user.check_password(password):
                return user
            else:
                return None

