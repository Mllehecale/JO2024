from django.test import TestCase
from JoBooking.models import CustomUser, Offre

# code lancement du test =   python manage.py test JoBooking.tests.test_nom_file
# BUT : VERIFICATION SI ENREGISTREMENT DATA DANS BDD


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
            is_staff=False,
            cle_inscription='t1e2s3t'
        )
        assert CustomUser.objects.filter(email='usertest@mail.com').exists()  # verifie si dans la BDD
        assert user.first_name == 'user'
        assert user.last_name == 'test'
        assert user.is_superuser is False  # verifie si attribut par défaut pris en compte
        assert user.is_staff is False
        assert user.cle_inscription == 't1e2s3t'

    # test inscription  avec données non valides
    def test_create_user_invalid_data(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email='usertest',  # email ne possède pas @.
                password='password',
                username='',
                first_name='user',  # ne doit prendre qque les str
                last_name=2,  # ne doit prendre que les str
                is_superuser=False,
                is_staff=False,
                cle_inscription=''
            )
        assert not CustomUser.objects.filter(
            email='usertest').exists()  # vérifie si creation dans BDD si oui echec test


#  test creation d'une offre
class TestCreateOffre(TestCase):
    def test_create_offre(self):
        offre = Offre.objects.create(
            title="offretest",
            price=6,
            description="offre test",
            billet=1,
            ventes=0
        )
        offre = Offre.objects.filter(title='offretest').exists()
        self.assertTrue(offre, 'la creation a échoué')
