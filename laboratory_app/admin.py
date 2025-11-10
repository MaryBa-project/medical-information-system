from django.contrib import admin
from .models import ResultAnalysis, TemplateParameter, TypeAnalysis, MedReferral, ResultParameter




# --- 1. Inline для дочірньої моделі (Параметри) ---
class ResultParameterInline(admin.TabularInline):
    """
    Дозволяє редагувати ResultParameter безпосередньо 
    на сторінці ResultAnalysis.
    """
    model = ResultParameter
    # Поля, які будуть відображатися та редагуватися в інлайні
    fields = ('template', 'value', 'unit_of_measurement', 'coment')
    # Додаємо автозаповнення полів з шаблону
    readonly_fields = ('unit_of_measurement',) # Це поле краще заповнювати автоматично
    extra = 1 # Кількість порожніх форм для додавання нових параметрів





# --- 2. Admin для батьківської моделі (Загальний Висновок) ---
@admin.register(ResultAnalysis)
class ResultAnalysisAdmin(admin.ModelAdmin):
    """
    Основна сторінка редагування, яка включає інлайни параметрів.
    """
    
    list_display = (
        'id', 
        'medcard_display', 
        'referral', 
        'lab_assistent', 
        'providing_date', 
        'report'
    )
    
    list_filter = ('providing_date', 'lab_assistent')
    search_fields = (
        'medcard__id', 
        'referral__id', 
        'lab_assistent__tab_nomer', 
        'report'
    )
    
    # Визначаємо, які поля відображаються у формі ResultAnalysis
    fields = (
        'medcard', 
        'referral', 
        'lab_assistent', 
        'report'
    )
    
    # ДОДАЄМО INLINE! Це магічна лінія, яка приєднує таблицю ResultParameter
    inlines = [ResultParameterInline]
    
    # Допоміжні методи для відображення
    def medcard_display(self, obj):
        # Припускаємо, що MedCards має метод display_id
        return obj.medcard.display_id()
    medcard_display.short_description = 'Мед. Картка ID'

    def report_summary(self, obj):
        # Показуємо лише перші 50 символів висновку
        return obj.report[:50] + '...' if obj.report and len(obj.report) > 50 else obj.report
    report_summary.short_description = 'Висновок'



admin.site.register(TemplateParameter)
admin.site.register(TypeAnalysis)
admin.site.register(MedReferral)
