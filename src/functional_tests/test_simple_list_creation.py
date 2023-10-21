from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    """Test for new visitor"""

    def test_can_start_a_list_for_one_user(self):
        # Open project home page
        self.browser.get(self.live_server_url)

        # Home page title says that it is To-Do project
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # You can write first To-Do line
        input_box = self.get_item_input_box()
        self.assertEquals(input_box.get_attribute("placeholder"), "Enter a to-do item")

        # Write "Buy milk"
        # When click Enter. On page, we have new line "1: Buy milk"
        self.add_list_item("Buy milk")

        # On page, you can write another To-Do line
        # Write "Make milkshake"
        self.add_list_item("Make milkshake")
        self.wait_for_row_in_list_table("1: Buy milk")

        # Page reload again and show two To-Do line

        # Site must generate uniq URL for user and show some text with information about that
        # self.fail("Complete test!")

        # When click on that URL user can see him list To-Do

        # End test session

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)

        self.add_list_item("Buy milk")

        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, "lists/.+")

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy milk", page_text)

        self.add_list_item("Make lunch")

        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, "lists/.+")
        self.assertNotEquals(first_user_list_url, second_user_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Make lunch", page_text)
        self.assertNotIn("Buy milk", page_text)
