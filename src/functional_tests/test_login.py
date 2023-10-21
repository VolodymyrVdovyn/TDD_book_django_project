import os
import poplib
import re
import time

from accounts.views import SEND_MAIL_SUBJECT, SEND_MAIL_SUCCESS_MESSAGE
from django.core import mail
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest

# TEST_EMAIL = "test@example.com"


class LoginTest(FunctionalTest):
    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL("pop.gmail.com")
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ["MAIL_PASSWORD"])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print("getting msg", i)
                    _, lines, __ = inbox.retr(i)
                    lines = [line.decode("utf8") for line in lines]
                    # print(lines)
                    if f"Subject: {subject}" in lines:
                        email_id = i
                        body = "\n".join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        if self.staging_server:
            TEST_EMAIL = os.environ["MAIL_LOGIN"]
        else:
            TEST_EMAIL = "test@example.com"

        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
        self.browser.find_element(By.NAME, "email").send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertIn(
                SEND_MAIL_SUCCESS_MESSAGE,
                self.browser.find_element(By.TAG_NAME, "body").text,
            )
        )

        body = self.wait_for_email(TEST_EMAIL, SEND_MAIL_SUBJECT)
        # email = mail.outbox[0]
        # self.assertIn(TEST_EMAIL, email.to)
        # self.assertEqual(email.subject, SEND_MAIL_SUBJECT)

        self.assertIn("Use this link to log in", body)
        url_search = re.search(r"http://.+/.+/.+/", body)

        if not url_search:
            self.fail(f"Could not find url in email body:\n{body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        self.browser.find_element(By.LINK_TEXT, "Log out").click()

        self.wait_to_be_logged_out(email=TEST_EMAIL)
