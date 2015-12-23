from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError


class SumFormula(models.Model):
    formula = models.TextField(primary_key=True)
    monoisotopic_mass = models.FloatField(default=0.0) #monoisotopic mass
    molecular_weight = models.FloatField(default=0.0) #average molecular weight

    def get_mass(self):
        mass = 0.0
        weight=0.0
        return mass,weight

    def validate_unique(self, exclude=None):
        qs = SumFormula.objects.filter(formula=self.formula)
        if qs.exists():
            raise ValidationError('Formula must be unique')

    def save(self, *args, **kwargs):
        self.validate_unique()
        self.monoisotopic_mass, self.molecular_weight = self.get_mass()
        super(SumFormula, self).save(*args, **kwargs)

    def __str__(self):
        return self.formula


class Molecules(models.Model):
    name = models.TextField(default="")
    formula = models.ForeignKey(SumFormula,null=True)
    def __str__(self):
        return self.name