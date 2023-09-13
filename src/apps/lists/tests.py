from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
    def test_uses_home_page(self):
        response = self.client.get("/")
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


class ListViewTest(TestCase):
    def test_uses_list_page(self):
        response = self.client.get("/lists/unique-list")
        self.assertTemplateUsed(response, "list.html")

    def test_display_all_items(self):
        Item.objects.create(text="First item")
        Item.objects.create(text="Second item")

        response = self.client.get("/lists/unique-list")

        self.assertContains(response, "First item")
        self.assertContains(response, "Second item")


class NewListTest(TestCase):
    def test_can_save_POST_request(self):
        input_value = "A new item in list"
        self.client.post("/lists/new", data={"item_text": input_value})
        self.assertEquals(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEquals(new_item.text, input_value)

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "something"})
        self.assertRedirects(response, "/lists/unique-list")
