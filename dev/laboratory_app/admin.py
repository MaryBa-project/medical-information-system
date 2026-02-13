from django.contrib import admin
from .models import ResultAnalysis, TemplateParameter, TypeAnalysis, MedReferral, ResultParameter




class ResultParameterInline(admin.TabularInline):
    """
    Дозволяє редагувати ResultParameter безпосередньо 
    на сторінці ResultAnalysis.
    """
    model = ResultParameter
    fields = ('template', 'value', 'unit_of_measurement', 'coment')
    readonly_fields = () 
    extra = 1

    # --- 2. Admin для батьківської моделі (Загальний Висновок) ---
@admin.register(ResultAnalysis)
class ResultAnalysisAdmin(admin.ModelAdmin):
    inlines = [ResultParameterInline]
    def save_formset(self, request, form, formset, change):
        """
        Перезаписуємо для автоматичного заповнення одиниці вимірювання
        на основі вибраного шаблону.
        """
        if formset.model == ResultParameter:
            instances = formset.save(commit=False)
            
            # Збереження всіх змінених/нових інстансів inline
            for instance in instances:
                # 1. Перевіряємо, чи був вибраний шаблон
                if instance.template:
                    try:
                        unit = instance.template.unit_of_measurement
                        instance.unit_of_measurement = unit
                        
                    except AttributeError:
                        instance.unit_of_measurement = 'ПОМИЛКА'
                instance.save()
            formset.save_m2m()
            for obj in formset.deleted_objects:
                obj.delete()
        else:
            super().save_formset(request, form, formset, change)

admin.site.register(TemplateParameter)
admin.site.register(TypeAnalysis)
admin.site.register(MedReferral)
