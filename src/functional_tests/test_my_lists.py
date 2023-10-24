from django.conf import settings
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest
from functional_tests.management.commands.create_session import create_pre_authenticated_session

User = get_user_model()

TEST_EMAIL = "test@example.com"


class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            from functional_tests.server_tools import create_session_on_server

            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(name=settings.SESSION_COOKIE_NAME, value=session_key, path="/"))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.create_pre_authenticated_session(TEST_EMAIL)
        self.browser.get(self.live_server_url)

        self.add_list_item("First list item")
        self.add_list_item("Second list item")

        first_list_url = self.browser.current_url

        self.browser.find_element(By.LINK_TEXT, "My lists").click()

        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, "First list item"))
        self.browser.find_element(By.LINK_TEXT, "First list item").click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        self.browser.get(self.live_server_url)
        self.add_list_item("Another list item")
        second_list_url = self.browser.current_url

        self.browser.find_element(By.LINK_TEXT, "My lists").click()

        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, "Another list item"))
        self.browser.find_element(By.LINK_TEXT, "Another list item").click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        self.browser.find_element(By.LINK_TEXT, "Log out").click()
        self.wait_for(lambda: self.assertEqual(self.browser.find_elements(By.LINK_TEXT, "My lists"), []))
