from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings


# méthode pour créer  user personnalisé
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:  # vérifie si l'email est saisi
            raise ValueError("Vous devez entrer un email valide.")
        email = self.normalize_email(email)  # email en minuscule
        user = self.model(email=email, **extra_fields)  # création d'une instance
        user.set_password(password)  # définition du Mot de passe , méthode pour ne pas l'afficher en clair dans BDD
        user.save(using=self._db)  # Enregistrement dans BDD
        return user  # retourner user pour effectuer autres opérations

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=130, blank=True, default='')
    first_name = models.CharField(max_length=130, blank=True, default='')
    last_name = models.CharField(max_length=130, blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    cle_inscription = models.CharField(max_length=100,blank=True,unique=True,null=True)


    objects = CustomUserManager()  # relie la classe CustomuserManager à ce modèle

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True


#  méthode pour créer les offres des jeux olympiques + compteur de ventes pour chaque offre

class Offre(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    billet = models.IntegerField(default=1)
    ventes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def ajout_vente(self):
        self.ventes += 1
        self.save()


# commande(s) passé(e)s par user
class Commande(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.offre.title}({self.quantity})'


class Reservation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)  # user peut avoir qu'un seul panier (réservation)
    commandes = models.ManyToManyField(Commande)
    paiement = models.BooleanField(default=False)
    date_commande = models.DateTimeField(blank=True, null=True)
    cle_paiement = models.CharField(max_length=100,unique=True,blank=True,null=True)

    # champs ManyToManyField non pris en charge pour champ interface admin donc voici une méthode personnalisée
    # sinon retourne ERROR  (admin.E109)
    def commandes_list(self):
        return '|'.join(commande.offre.title for commande in self.commandes.all())

    def __str__(self):
        return self.user.email  # rappel : l'email est une donnée unique

