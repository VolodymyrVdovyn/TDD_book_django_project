from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_page(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "lists/home.html")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}")
        self.assertTemplateUsed(response, "lists/list.html")

    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="First item", list=correct_list)
        Item.objects.create(text="Second item", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="Other First item", list=other_list)
        Item.objects.create(text="Other Second item", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}")

        self.assertContains(response, "First item")
        self.assertContains(response, "Second item")
        self.assertNotContains(response, "Other First item")
        self.assertNotContains(response, "Other Second item")

    def test_ref(self):
        correct_list = List.objects.create()
        List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}")
        self.assertEqual(response.context["list"], correct_list)


class NewListTest(TestCase):
    def test_can_save_POST_request(self):
        input_value = "A new item in list"
        self.client.post("/lists/new", data={"item_text": input_value})
        self.assertEquals(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEquals(new_item.text, input_value)

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "something"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}")


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_existing_list(self):
        correct_list = List.objects.create()
        List.objects.create()

        self.client.post(f"/lists/{correct_list.id}/add-item", data={"item_text": "New item"})

        self.assertEqual(Item.objects.count(), 1)

        item = Item.objects.first()
        self.assertEqual(item.text, "New item")
        self.assertEqual(item.list, correct_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()
        List.objects.create()

        response = self.client.post(f"/lists/{correct_list.id}/add-item", data={"item_text": "New item"})

        self.assertRedirects(response, f"/lists/{correct_list.id}")
