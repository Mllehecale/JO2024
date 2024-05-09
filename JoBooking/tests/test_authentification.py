from django.test import TestCase, Client
from JoBooking.models import CustomUser
from JoBooking.views import CustomSignupForm


# code lancement du test =   python manage.py test JoBooking.tests.test_nom_file
# BUT  VERIFICATION DE L'AUTHENTIFICATION DE L'USER
class TestAuthentification(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = CustomUser.objects.create_user(email='test@test.com', password='testtest')

    # test de connexion avec données valides.
    def test_connexion_valid_data(self):
        response = self.client.post("/connexion/", {'email': 'test@test.com', 'password': 'testtest'})
        self.assertRedirects(response, "/", status_code=302)  # ici on s'attend a une redirection vers page dacceuil

        # test de connexion avec données invalides.

    def test_connexion_invalid_data(self):
        response = self.client.post("/connexion/", {'email': 'testtest.com', 'password': 'testes'})
        self.assertContains(response, 'Identifiants non valides.', status_code=200, msg_prefix='', html=True, count=0)
        # user qui met donnés invalides verra  'Identifiants non valides.' sur l'interface


class TestInscriptionAuthentification(TestCase):
    def setUp(self):
        self.client = Client()

        # test qui verifie si form valide lors de l'inscription, renvoie vers la page verification email
    def test_inscription_verification_email(self):
        user_form = {
            'first_name': 'user',
            'last_name': 'test',
            'email': 'usertest@mail.com',
            'password1': 'u1u1u1tt',
            'password2': 'u1u1u1tt'
        }
        form = CustomSignupForm(data=user_form)
        self.assertTrue(form.is_valid(), msg=f"Form errors:{form.errors}")

        # assert CustomUser.objects.filter(email='usertest@mail.com').exists()
        response = self.client.post("/inscription/", data=user_form)
        self.assertRedirects(response, "/verification_email/", status_code=302)


class TestDeconnexion(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@test.com', password='testtest')

    # test qui verifie si l'user est deconnecte
    def test_user_deconnexion(self):
        self.client.post("/connexion/", {'email': 'test@test.com', 'password': 'testtest'})
        self.client.get("/deconnexion/")

        self.assertNotIn('_auth_user_id', self.client.session)
        # verification si présence de l'idenfifiant de l'user connecté dans session
