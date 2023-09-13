import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

MAX_WAIT = 3


class NewVisitorTest(LiveServerTestCase):
    """Test for new visitor"""

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # Open project home page
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table("1: Buy milk")

        # On page, you can write another To-Do line
        # Write "Make milkshake"
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Make milkshake")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make milkshake")

        # Page reload again and show two To-Do line

        # Site must generate uniq URL for user and show some text with information about that
        # self.fail("Complete test!")

        # When click on that URL user can see him list To-Do

        # End test session

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Buy milk")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, 'lists/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy milk", page_text)

        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Make lunch")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Make lunch")

        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, 'lists/.+')
        self.assertNotEquals(first_user_list_url, second_user_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Make lunch", page_text)
        self.assertNotIn("Buy milk", page_text)







