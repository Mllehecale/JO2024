from django.test import TestCase, Client
from JoBooking.models import CustomUser
from JoBooking.views import CustomSignupForm


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
        self.assertContains(response, 'Identifiants non valides.', status_code=200, msg_prefix='', html=True, count=1)
        print(response.content)


class TestInscriptionAuthentification(TestCase):
    def setUp(self):
        self.client = Client()
        # self.user = CustomUser.objects.create_user(email='usertest@mail.com', password='password', first_name='user',
        # last_name='test')
        # Test qui vérifie si user redirigé vers page vérification email pour poursuivre inscription

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


