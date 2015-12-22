_author__ = 'palmer'
import time
from django.test import LiveServerTestCase
from django.http import HttpRequest
from selenium import webdriver
import unittest
from spec_browse.views import home_page, mol_detail
from spec_browse.models import Molecules

class AdminVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
    # Load admin page
    def test_get_admin_site(self):
        self.browser.get('http://localhost:8000/admin/')
        self.assertIn('Django', self.browser.title)


class HomePageTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def make_models(self):
        first_item = Molecules()
        first_item.name = 'Molecule 1'
        first_item.save()
        second_item = Molecules()
        second_item.name = 'Molecule 2'
        second_item.save()

    def tearDown(self):
        self.browser.quit()

    def test_get_home_page(self):
        # Load home page
        self.make_models()
        saved_items = Molecules.objects.all()
        self.assertEqual(saved_items.count(),2)
        self.browser.get(self.live_server_url)
        self.assertIn('spectral browser', self.browser.title)
        # See a list of <some> molecules #todo: some->more defined (e.g. 5)
        request = HttpRequest()
        response = home_page(request)
        self.assertIn('Molecule 1', response.content.decode())
        self.assertIn('Molecule 2', response.content.decode())
        # check molcules have links
        url_to_follow = "/detail/mol1" #todo: get this from a link tag?
        self.assertIn(url_to_follow,response.content.decode())
        # Clicks on a molecule
        # Goes to the detail page for the molecule
        # Can see some detail
        response = mol_detail(HttpRequest,1)
        self.assertIn('Molecule Detail', response.content.decode())
if __name__ == '__main__':
    unittest.main()