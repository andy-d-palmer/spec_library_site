from __future__ import unicode_literals

from django.db import models
import sys
sys.path.append("//Users/palmer/Documents/python_codebase/")
from pyMS.pyisocalc import pyisocalc
import numpy as np

class SumFormula(models.Model):
    formula = models.TextField(primary_key=True)
    monoisotopic_mass = models.FloatField(default=0.0) #monoisotopic mass
    molecular_weight = models.FloatField(default=0.0) #average molecular weight

    def get_mass(self):
        spec = pyisocalc.isodist(self.formula,charges=0,do_centroid=False)
        mass = spec.get_spectrum(source='centroids')[0][np.argmax(spec.get_spectrum(source='centroids')[1])]
        weight=np.average(spec.get_spectrum(source='centroids')[0],weights=spec.get_spectrum(source='centroids')[1])
        return mass,weight

    def validate_unique(self, exclude=None):
        qs = SumFormula.objects.filter(formula=self.formula)
        #if qs.exists():
        #    raise ValidationError('Formula must be bloody unique')

    def save(self, *args, **kwargs):
        #self.validate_unique()
        self.monoisotopic_mass, self.molecular_weight = self.get_mass()
        super(SumFormula, self).save(*args, **kwargs)

    def __str__(self):
        return self.formula


class Molecules(models.Model):
    name = models.TextField(default="<empty>")
    formula = models.ForeignKey(SumFormula,null=True)

    def __str__(self):
        return self.name


class Ion(models.Model):
    def __str__(self):
        return "{} {}".format(self.molecule,self.adduct)

    def save(self,*args,**kwargs):
        self.mono_mz = self.get_monoiso_mz()
        super(Ion, self).save(*args, **kwargs)

    def get_monoiso_mz(self):
        spec = pyisocalc.isodist(pyisocalc.complex_to_simple(self.molecule.formula.formula + self.adduct),charges=0,do_centroid=False)
        mass = spec.get_spectrum(source='centroids')[0][np.argmax(spec.get_spectrum(source='centroids')[1])]
        return mass

    adduct = models.TextField(default="+H")
    molecule = models.ForeignKey(Molecules, default=Molecules(name="").save())
    charge = models.IntegerField(default=1)
    mono_mz = models.FloatField(default=0.0)




