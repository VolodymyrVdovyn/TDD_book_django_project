from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(input_box.location["x"] + (input_box.size["width"] / 2), 512, delta=10)

        input_box.send_keys("Testing")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Testing")

        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(input_box.location["x"] + (input_box.size["width"] / 2), 512, delta=10)
