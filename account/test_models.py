from django.test import TestCase
from .models import Account

class AccountModelTestCase(TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.username = 'testuser'
        self.password = 'password'
        self.user = Account.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )

    def test_user_creation(self):
        user = Account.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )
        self.assertTrue(Account.objects.filter(email=self.email).exists())

    def test_user_deletion(self):
        user = Account.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )
        user.delete()
        self.assertFalse(Account.objects.filter(email=self.email).exists())