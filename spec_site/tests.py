_author__ = 'palmer'
import time
from django.test import LiveServerTestCase
from django.http import HttpRequest
from selenium import webdriver
import unittest
from spec_browse.views import home_page, mol_detail, sf_detail, ion_detail
from spec_browse.models import Molecules, SumFormula, Ion

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


class BasicPageViews(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def make_models(self):
        SumFormula(formula="C7H8O9").save()
        SumFormula(formula="C10H10O10").save()
        Molecules(name = 'Molecule 1', formula = SumFormula.objects.all().get(formula='C7H8O9')).save()
        Molecules(name = 'Molecule 2', formula = SumFormula.objects.all().get(formula='C10H10O10')).save()
        Molecules(name = 'Molecule 3', formula = SumFormula.objects.all().get(formula='C10H10O10')).save()
        Ion(adduct = '+H',  molecule = Molecules.objects.all().get(name='Molecule 1'), charge = 1).save()
        Ion(adduct = '+Na', molecule = Molecules.objects.all().get(name='Molecule 1'), charge = 1).save()
        Ion(adduct = '+K',  molecule = Molecules.objects.all().get(name='Molecule 1'), charge = 1).save()

    def tearDown(self):
        self.browser.quit()

    def test_get_home_page(self):
        # Load home page
        self.make_models()
        saved_items = Molecules.objects.all()
        self.assertEqual(saved_items.count(),3)
        self.browser.get(self.live_server_url)
        self.assertIn('spectral browser', self.browser.title)
        # See a list of <some> molecules #todo: some->more defined (e.g. 5)
        request = HttpRequest()
        response = home_page(request)
        self.assertIn('Molecule 1', response.content.decode())
        self.assertIn('Molecule 2', response.content.decode())
        # check molcules have links
        url_to_follow = "/mol/mol1" #todo: get this from a link tag?
        self.assertIn(url_to_follow,response.content.decode())
        # Clicks on a molecule
        # Goes to the detail page for the molecule
        # Can see some detail
        response = mol_detail(HttpRequest,1)
        self.assertIn('Molecule Detail', response.content.decode())

    def test_get_sum_formula(self):
        # Open page for a SumFormula. Check that all molecules with that sum formula are shown
        self.make_models()
        sf_to_follow = "C10H10O10" #todo: get this from a link tag?
        response = sf_detail(HttpRequest,sf_to_follow)
        self.assertIn(sf_to_follow, response.content.decode())
        self.assertIn('C10H10O10', response.content.decode())

    def test_get_ion(self):
        self.make_models()
        pk_to_follow = [str(ion.pk) for ion in Ion.objects.all()][0]
        response = ion_detail(HttpRequest,pk_to_follow)
        self.assertIn(pk_to_follow, response.content.decode())
        self.assertIn('C7H8O9', response.content.decode())

if __name__ == '__main__':
    unittest.main()