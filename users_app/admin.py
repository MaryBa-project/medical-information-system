from django.contrib import admin
from .models import Doctor, Personnel, Patient, LaboratoryAssistent, CustomUser, FamilyDoctor


admin.site.register(CustomUser)
admin.site.register(Doctor)
admin.site.register(Personnel)
admin.site.register(Patient)
admin.site.register(LaboratoryAssistent)
admin.site.register(FamilyDoctor)
