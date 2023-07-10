from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
    def test_uses_home_page(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_POST_request(self):
        input_value = "A new item in list"
        response = self.client.post("/", data={"item_text": input_value})
        self.assertIn(input_value, response.content.decode())
        self.assertTemplateUsed(response, "home.html")


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "First item"
        first_item.save()

        second_item = Item()
        second_item.text = "Second item"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEquals(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEquals(first_saved_item.text, "First item")
        self.assertEquals(second_saved_item.text, "Second item")
