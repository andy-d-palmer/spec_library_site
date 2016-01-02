from django.contrib import admin
from .models import Molecules, SumFormula, Ion

admin.site.register(Molecules)
admin.site.register(SumFormula)
admin.site.register(Ion)