from django.test import TestCase
from django.utils.html import escape
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_page(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "lists/home.html")

    def test_home_page_uses_item_form(self):
        response = self.client.get("/")
        self.assertIsInstance(response.context["form"], ItemForm)


class ListViewTest(TestCase):
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(f"/lists/{list_.id}", data={"text": ""})

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

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}")
        self.assertEqual(response.context["list"], correct_list)

    def test_can_save_a_POST_request_to_existing_list(self):
        correct_list = List.objects.create()
        List.objects.create()

        self.client.post(f"/lists/{correct_list.id}", data={"text": "New item"})

        self.assertEqual(Item.objects.count(), 1)

        item = Item.objects.first()
        self.assertEqual(item.text, "New item")
        self.assertEqual(item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        correct_list = List.objects.create()
        List.objects.create()

        response = self.client.post(f"/lists/{correct_list.id}", data={"text": "New item"})

        self.assertRedirects(response, f"/lists/{correct_list.id}")

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lists/list.html")

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}")
        self.assertIsInstance(response.context["form"], ItemForm)


class NewListTest(TestCase):
    def test_can_save_POST_request(self):
        input_value = "A new item in list"
        self.client.post("/lists/new", data={"text": input_value})
        self.assertEquals(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEquals(new_item.text, input_value)

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"text": "something"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}")

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lists/home.html")

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertIsInstance(response.context["form"], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
