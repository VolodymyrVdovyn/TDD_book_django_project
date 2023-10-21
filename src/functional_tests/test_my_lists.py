from django.contrib.auth import get_user_model, BACKEND_SESSION_KEY, SESSION_KEY
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore

from functional_tests.base import FunctionalTest

User = get_user_model()

TEST_EMAIL = "test@example.com"


class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(name=settings.SESSION_COOKIE_NAME, value=session.session_key, path="/"))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(TEST_EMAIL)

        self.create_pre_authenticated_session(TEST_EMAIL)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(TEST_EMAIL)
