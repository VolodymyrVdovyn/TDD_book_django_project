from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest
from lists.forms import DUPLICATE_ITEM_ERROR


class ItemValidationTest(FunctionalTest):
    @property
    def get_error_element(self):
        return self.browser.find_element(By.CSS_SELECTOR, ".has-error")

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid"))

        self.get_item_input_box().send_keys("Buy milk")
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:valid"))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid"))

        self.get_item_input_box().send_keys("Make tea")
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:valid"))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")

    def test_cannot_add_duplicate_list_items(self):
        self.browser.get(self.live_server_url)

        self.get_item_input_box().send_keys("Buy milk")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        self.get_item_input_box().send_keys("Buy milk")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(self.get_error_element.text, DUPLICATE_ITEM_ERROR))

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)

        self.get_item_input_box().send_keys("Buy milk")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        self.get_item_input_box().send_keys("Buy milk")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertTrue(self.get_error_element.is_displayed()))

        self.get_item_input_box().send_keys("a")
        self.wait_for(lambda: self.assertFalse(self.get_error_element.is_displayed()))
