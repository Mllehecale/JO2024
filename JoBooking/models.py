from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:  # vérifie si l'email est saisi
            raise ValueError("Vous devez entrer un email valide.")
        email = self.normalize_email(email)  # email en minuscule
        user = self.model(email=email, **extra_fields)  # création d'une instance
        user.set_password(password)  # définition du Mot de passe , méthode pourne pas l'afficher en clair dans BDD
        user.save(using=self._db)  # Enregistrement dans BDD
        return user  # retourner user pour effectuer autres opérations

    def create_superuser(self, email=None, password=None, **extra_fields):
        user = self._create_user(email=email, password=password, **extra_fields)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=130, blank=True, default='')
    first_name = models.CharField(max_length=130, blank=True, default='')
    last_name = models.CharField(max_length=130, blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()  # relie la classe CustomuserManager à ce modèle

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['username']
