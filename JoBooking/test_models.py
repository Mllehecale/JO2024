from django.test import TestCase
from .models import CustomUserManager, CustomUser


# test creation user avec données valides
class TestCustomUserManager(TestCase):
    def test_create_user(self):
        user1 = CustomUser.objects.create_user(
            email='user1@mail.com',
            username='',
            first_name='leo',
            last_name='lebourdon',
            is_superuser=False,
            is_active=True,
            is_staff=False
        )
        self.assertEqual(user1.email, 'user1@mail.com')
        self.assertEqual(user1.username, '')
        self.assertEqual(user1.first_name, 'leo')
        self.assertEqual(user1.last_name, 'lebourdon')
        self.assertEqual(user1.is_superuser, False)
        self.assertEqual(user1.is_active, True)
        self.assertEqual(user1.is_staff, False)
