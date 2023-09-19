from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_page(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "First item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Second item"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEquals(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEquals(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        self.assertEquals(first_saved_item.text, "First item")
        self.assertEquals(first_saved_item.list, list_)

        second_saved_item = saved_items[1]
        self.assertEquals(second_saved_item.text, "Second item")
        self.assertEquals(second_saved_item.list, list_)


class ListViewTest(TestCase):
    def test_uses_list_page(self):
        response = self.client.get("/lists/unique-list")
        self.assertTemplateUsed(response, "list.html")

    def test_display_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="First item", list=list_)
        Item.objects.create(text="Second item", list=list_)

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
