import time
import unittest
from logging import warning

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):
    """Test for new visitor"""

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Open project home page
        self.browser.get("http://localhost:8000")

        # Home page title says that it is To-Do project
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # You can write first To-Do line
        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertEquals(input_box.get_attribute("placeholder"), "Enter a to-do item")

        # Write "Buy milk"
        # When click Enter. On page, we have new line "1: Buy milk"
        input_box.send_keys("Buy milk")
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table("1: Buy milk")

        # On page, you can write another To-Do line
        # Write "Make milkshake"
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Make milkshake")
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table("1: Buy milk")
        self.check_for_row_in_list_table("2: Make milkshake")

        # Page reload again and show two To-Do line

        # Site must generate uniq URL for user and show some text with information about that
        self.fail("Complete test!")

        # When click on that URL user can see him list To-Do

        # End test session


if __name__ == "__main__":
    unittest.main(warnings="ignore")
