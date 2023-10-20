import re

from accounts.views import SEND_MAIL_SUCCESS_MESSAGE, SEND_MAIL_SUBJECT
from django.core import mail
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest

TEST_EMAIL = "test@example.com"


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):

        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
        self.browser.find_element(By.NAME, "email").send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertIn(
                SEND_MAIL_SUCCESS_MESSAGE,
                self.browser.find_element(By.TAG_NAME, "body").text,
            )
        )

        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SEND_MAIL_SUBJECT)

        self.assertIn("Use this link to log in", email.body)
        url_search = re.search(r"http://.+/.+/.+/", email.body)

        if not url_search:
            self.fail(f"Could not find url in email body:\n{email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)
        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, "Log out"))
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertIn(TEST_EMAIL, navbar.text)

        self.browser.find_element(By.LINK_TEXT, "Log out").click()

        self.wait_for(lambda : self.browser.find_element(By.NAME, "email"))
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertNotIn(TEST_EMAIL, navbar.text)

