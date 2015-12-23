from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Molecules(models.Model):
    name = models.TextField(default="")

    def __str__(self):
        return self.name

