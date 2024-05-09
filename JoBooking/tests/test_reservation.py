from django.test import TestCase, Client
from JoBooking.models import CustomUser, Commande, Offre
import uuid


# code lancement du test =   python manage.py test JoBooking.tests.test_nom_file

class TestCommande(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@test.com', password='testtest',
                                                   first_name='user', last_name='test')

    # test verifie si redirection vers page connexion si user non connecté
    def test_connexion_requis_panier(self):
        response = self.client.get("/commande/")
        self.assertRedirects(response, "/connexion/?next=/commande/", status_code=302)

    # test qui verifie  pdf generee quand le paiement = True
    def test_verification_PDF_genere_transaction(self):
        offre = Offre.objects.create(title='offretest', price=2, id=5)  # parametre necessaire  pour creer le pdf
        date = "datetest"  # parametre necessaire  pour creer le pdf
        commande = Commande.objects.create(user=self.user, paiement=True, offre=offre)
        if commande.paiement is True:
            cle_paiement = uuid.uuid4().hex  # parametre necessaire  pour creer le pdf
            commande.cle_paiement = cle_paiement
            commande.save()
        self.client.force_login(self.user)  # connexion de l'user
        response = self.client.get("/telechargement_pdf/")
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertNotEqual(response.content, b'')

    # test qui verifie si renvoi vers page panier vide si pas encore de commande
    def test_renvoi_panier_vide(self):
        self.client.force_login(self.user)
        response = self.client.get("/commande/")
        self.assertTemplateUsed(response, "panier_vide.html")

    # test qui annulation d'un panier
    def test_annulation_commande(self):
        self.client.force_login(self.user)
        offre = Offre.objects.create(title='offretest', price=2, id=5)
        Commande.objects.create(user=self.user, paiement=False, offre=offre)
        response = self.client.get("/commande/annulation")
        self.assertRedirects(response, "/")  # doit rediriger vers page d'acceuil


class TestPaiement(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@test.com', password='testtest')

    # test si cle paiement generee quand user paye
    def test_cle_paiement_transaction_user(self):
        offre = Offre.objects.create(title='offretest', price=2, id=5)
        commande = Commande.objects.create(user=self.user, paiement=False, offre=offre)
        commande.paiement = True
        if commande.paiement is True:
            cle_paiement = uuid.uuid4().hex
            commande.cle_paiement = cle_paiement
            commande.save()

        self.client.force_login(self.user)
        self.client.post("/commande/payer")
        self.assertTrue(commande.paiement)
        self.assertIsNotNone(commande.cle_paiement)
