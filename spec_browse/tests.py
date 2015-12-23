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

from spec_browse.models import Molecules, SumFormula

from django.core.exceptions import ValidationError

class MoleculeModelTest(TestCase):
    def test_saving_and_returning_molecule(self):
        Molecules(name = "my first molecule").save()
        Molecules(name = "out of nowhere... another molecule").save()
        saved_items = Molecules.objects.all()
        self.assertEqual(saved_items.count(),2)
        first_saved_item = saved_items[0]
        self.assertEqual(first_saved_item.name,"my first molecule")
        second_saved_item = saved_items[1]
        self.assertEqual(second_saved_item.name,"out of nowhere... another molecule")

    def test_saving_molecule_with_formula(self):
        third_molecule = Molecules(name='another molecule', formula = SumFormula(formula="C7H8O9").save())
        third_molecule.save()
        self.assertEqual(Molecules.objects.all().count(),1)
        self.assertEqual(SumFormula.objects.all().count(),1)

class SumFormulaModelTest(TestCase):
    def test_saving_and_returning_molecule(self):
        first_item = SumFormula(formula="C1H2O3")
        first_item.save()
        second_item = SumFormula(formula="C4H5O6")
        second_item.save()
        saved_items = SumFormula.objects.all()
        self.assertEqual(saved_items.count(),2)

    def test_primary_key(self):
        sf_to_dupliate = "C7H8O9"
        third_item = SumFormula(formula=sf_to_dupliate,mass=100.)
        third_item.save()
        fourth_item = SumFormula(formula=sf_to_dupliate)
        with self.assertRaises(ValidationError):
            fourth_item.save()


