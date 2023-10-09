from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


class ItemModelTest(TestCase):
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_)
        self.assertIn(item, list_.item_set.all())

    def test_default_item_text(self):
        item = Item()
        self.assertEqual(item.text, "")

    def test_items_in_list_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(text="First item", list=list_)
        item2 = Item.objects.create(text="Item 2", list=list_)
        item3 = Item.objects.create(text="3", list=list_)
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_item_string_representation(self):
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")

    def test_cannot_save_empty_item_in_list(self):
        list_ = List.objects.create()

        item = Item(text="", list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text="Duplicate", list=list_)
        with self.assertRaises(ValidationError):
            item = Item(text="Duplicate", list=list_)
            item.full_clean()
            # item.save()

    @staticmethod
    def test_CAN_save_same_items_to_different_lists():
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(text="Duplicate", list=list1)
        item = Item(text="Duplicate", list=list2)
        item.full_clean()


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}")
