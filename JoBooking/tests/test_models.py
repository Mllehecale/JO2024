from django.test import TestCase
from JoBooking.models import CustomUser


# test inscription avec données valides et obligatoires
class TestCreateUser(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email='usertest@mail.com',
            password='password',
            username='',
            first_name='user',
            last_name='test',
            is_superuser=False,
            is_staff=False
        )
        assert CustomUser.objects.filter(email='usertest@mail.com').exists()  # verifie si dans la BDD
        assert user.first_name == 'user'
        assert user.last_name == 'test'
        assert user.is_superuser is False  # verifie si attribut par défaut pris en compte
        assert user.is_staff is False


# test inscription  avec données non valides
# test connexion user avec True data
# test connexion user avec False data


# test qui verifie  http response = 200
class TestUrl(TestCase):
    def test_my_view(self):
        response = self.client.get('http://127.0.0.1:8000/')
        self.assertEqual(response.status_code, 200)
