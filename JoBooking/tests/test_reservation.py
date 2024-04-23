from django.test import TestCase, Client
from JoBooking.models import CustomUser, Commande, Offre
import uuid


class TestCommande(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@test.com', password='testtest')

    # test verifie si redirection vers page connexion si user non connecté
    def test_connexion_requis_panier(self):
        response = self.client.get("/commande/")
        self.assertRedirects(response, "/connexion/?next=/commande/", status_code=302)


class TestPaiement(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@test.com', password='testtest')

    def test_cle_paiement_transaction_user(self):
        offre = Offre.objects.create(title='offretest', price=2, id=5)
        commande = Commande.objects.create(user=self.user, paiement=False, offre=offre)
        commande.paiement = True
        if commande.paiement is True:
            cle_paiement = uuid.uuid4().hex
            commande.cle_paiement = cle_paiement
            commande.save()

        self.client.force_login(self.user)
        response = self.client.post("/commande/payer")

        self.assertTrue(commande.paiement)
        self.assertIsNotNone(commande.cle_paiement)
