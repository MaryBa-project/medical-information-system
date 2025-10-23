from django.contrib import admin
from .models import ResultAnalysis, TemplateParameter, TypeAnalysis, MedReferral, ResultParameter


admin.site.register(ResultParameter)
admin.site.register(ResultAnalysis)
admin.site.register(TemplateParameter)
admin.site.register(TypeAnalysis)
admin.site.register(MedReferral)
