from django.test import TestCase
from django.core.urlresolvers import resolve
# Create your tests here.
from django.http import HttpRequest
from views import home_page
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b"<!DOCTYPE html>"))
        self.assertTrue(response.content.endswith(b"</html>"))

from spec_browse.models import Molecules
class ItemModelTest(TestCase):

    def test_saving_and_returning_molecule(self):
        first_item = Molecules()
        first_item.name = "my first molecule"
        first_item.save()
        first_item = Molecules()
        first_item.name = "out of nowhere... another molecule"
        first_item.save()

        saved_items = Molecules.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        self.assertEqual(first_saved_item.name,"my first molecule")
        second_saved_item = saved_items[1]
        self.assertEqual(second_saved_item.name,"out of nowhere... another molecule")
