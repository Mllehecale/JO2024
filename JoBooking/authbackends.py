from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.backends import BaseBackend

""" méthode d'une authentification personnalisée . Elle  vérifie l'email et le mot de passe des utilisateurs 
qui sont récupérés à partir de leur identifiant (id) """

class EmailAuthBackend(BaseBackend):
    def authenticate(self,request, email=None, password=None):
        try:
            user=CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except ObjectDoesNotExist:
            raise ValueError("email invalide")


    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
