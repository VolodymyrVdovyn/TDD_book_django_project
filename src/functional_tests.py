from logging import warning
from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    """Test for new visitor"""

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Open prjoect home page
        self.browser.get('http://localhost:8000')

        # Home page title says that it is To-Do project
        self.assertIn("To-Do", self.browser.title)
        self.fail("Complete test!")

        # You can write first todo line

        # Write "Buy milk"

        # When click Enter. On page we have new line "1: Buy milk"

        # On page you can write another todo line
        # Write "Make milkshake"

        # Page reload again and show two todo line

        # Site must generate uniq URL for user and show some text with information about that

        # When click on that URL user can see him list todo

        # End test session

if __name__ == "__main__":
    unittest.main(warnings="ignore")

