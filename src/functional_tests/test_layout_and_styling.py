from selenium.webdriver import Keys

from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input_box = self.get_item_input_box()
        self.assertAlmostEqual(input_box.location["x"] + (input_box.size["width"] / 2), 512, delta=10)

        self.add_list_item("Testing")

        input_box = self.get_item_input_box()
        self.assertAlmostEqual(input_box.location["x"] + (input_box.size["width"] / 2), 512, delta=10)
