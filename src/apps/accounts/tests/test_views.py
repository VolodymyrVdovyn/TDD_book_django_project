from unittest.mock import call, patch
from uuid import UUID

import accounts.views
from accounts.models import Token
from accounts.views import SEND_MAIL_SUCCESS_MESSAGE, SEND_MAIL_SUBJECT
from django.test import TestCase

TEST_TOKEN = "00000000-0000-0000-0000-000000000000"
TEST_EMAIL = "test@example.com"


class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        self.send_mail_called = False
        self.subject, self.from_email, self.recipient_list = None, None, None

        def fake_send_mail(subject, message, from_email, recipient_list):
            self.send_mail_called = True
            self.subject = subject
            self.message = message
            self.from_email = from_email
            self.recipient_list = recipient_list

        accounts.views.send_mail = fake_send_mail

        response = self.client.post("/accounts/send_login_email/", data={"email": TEST_EMAIL})

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, SEND_MAIL_SUBJECT)
        self.assertEqual(self.from_email, "noreply@superlists")
        self.assertEqual(self.recipient_list, [TEST_EMAIL])
        self.assertRedirects(response, "/")

    @patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post("/accounts/send_login_email/", data={"email": TEST_EMAIL})

        self.assertTrue(mock_send_mail.called)

        subject, message, from_email, recipient_list = mock_send_mail.call_args.kwargs.values()
        self.assertEqual(subject, SEND_MAIL_SUBJECT)
        self.assertEqual(from_email, "noreply@superlists")
        self.assertEqual(recipient_list, [TEST_EMAIL])

        # mock_send_mail.assert_called_once_with(
        #     subject=SEND_MAIL_SUBJECT,
        #     message=f"Use this link to log in:\n\nurl",
        #     from_email="noreply@superlists",
        #     recipient_list=[TEST_EMAIL],
        # )

    def test_adds_success_message(self):
        response = self.client.post("/accounts/send_login_email/", data={"email": TEST_EMAIL}, follow=True)

        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            SEND_MAIL_SUCCESS_MESSAGE,
        )
        self.assertEqual(message.tags, "success")

    def test_creates_token_associated_with_email(self):
        self.client.post("/accounts/send_login_email/", data={"email": TEST_EMAIL})
        token = Token.objects.first()
        self.assertEqual(token.email, TEST_EMAIL)

    @patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post("/accounts/send_login_email/", data={"email": TEST_EMAIL})
        token = Token.objects.first()

        message = mock_send_mail.call_args.kwargs["message"]
        expected_url = f"http://testserver/accounts/login/{token.uid}/"

        self.assertIn(expected_url, message)


@patch("accounts.views.auth")
class LoginViewTest(TestCase):
    def test_redirects_to_home_page(self, mock_auth):
        response = self.client.get(f"/accounts/login/{TEST_TOKEN}/")

        self.assertRedirects(response, "/")

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get(f"/accounts/login/{TEST_TOKEN}/")

        self.assertEqual(mock_auth.authenticate.call_args, call(uid=UUID(TEST_TOKEN)))

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get(f"/accounts/login/{TEST_TOKEN}/")

        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value),
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None

        self.client.get(f"/accounts/login/{TEST_TOKEN}/")

        self.assertFalse(mock_auth.login.called)
