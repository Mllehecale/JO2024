from django.test import TestCase, Client
from JoBooking.models import CustomUser


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
