from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

TEST_EMAIL = "test@example.com"


class AuthenticationTest(TestCase):
    def test_returns_None_if_no_such_token(self):
        user = PasswordlessAuthenticationBackend().authenticate(None, "no-such-token")
        self.assertIsNone(user)

    def test_return_new_user_with_correct_email_if_token_exists(self):
        token = Token.objects.create(email=TEST_EMAIL)

        user = PasswordlessAuthenticationBackend().authenticate(None, token.uid)
        new_user = User.objects.get(email=TEST_EMAIL)

        self.assertEqual(user, new_user)

    def test_return_existing_user_with_correct_email_if_token_exists(self):
        token = Token.objects.create(email=TEST_EMAIL)
        existing_user = User.objects.create(email=TEST_EMAIL)

        user = PasswordlessAuthenticationBackend().authenticate(None, token.uid)

        self.assertEqual(user, existing_user)

    def test_get_user_by_email(self):
        User.objects.create(email="another@example.com")
        our_user = User.objects.create(email=TEST_EMAIL)

        user = PasswordlessAuthenticationBackend().get_user(TEST_EMAIL)

        self.assertEqual(user, our_user)

    def test_returns_None_if_no_user_with_that_email(self):
        self.assertIsNone(PasswordlessAuthenticationBackend().get_user(TEST_EMAIL))
