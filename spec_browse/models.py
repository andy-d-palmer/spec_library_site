from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Molecules(models.Model):
    name = models.TextField(default="")
    def __str__(self):
        return self.name

class SumFormula(models.Model):
    formula = models.TextField(primary_key=True)
    mass = models.FloatField(default=0.0)

    def validate_unique(self, exclude=None):
        qs = SumFormula.objects.filter(formula=self.formula)
        if qs.exists():
            raise ValidationError('Formula must be unique')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(SumFormula, self).save(*args, **kwargs)