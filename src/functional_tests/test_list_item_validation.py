from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("")
        input_box.send_keys(Keys.ENTER)

        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Buy milk")
        input_box.send_keys(Keys.ENTER)

        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("")
        input_box.send_keys(Keys.ENTER)

        self.fail("Write me!")
