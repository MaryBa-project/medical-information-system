from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Doctor, Personnel, Patient, LaboratoryAssistent, CustomUser, FamilyDoctor

class CustomUserAdmin(UserAdmin):
    # Додаємо до стандартних полів нові в форму додавання користувача
  add_fieldsets = UserAdmin.add_fieldsets + (
        ('Персональна інформація', {'fields': ('email','last_name', 'first_name', 
                                                'patronymic', 'groups', 'phone_number', 'img')}),
    )

    # Тут ми додаємо ТІЛЬКИ нові поля для кастом юзер, щоб уникнути дублювання email, first_name, last_name..
  fieldsets = UserAdmin.fieldsets + (
        ('Додаткова інформація профілю', {'fields': ('patronymic', 'phone_number', 'img')}),
    )


@admin.register(FamilyDoctor)
class FamilyDoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            kwargs["queryset"] = Doctor.objects.filter(specialization="Терапевт")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Patient)


# --- Базовий клас для генерації табельного номера ---

class BasePersonnelAdmin(admin.ModelAdmin):
    """Базовий клас для Doctor, Personnel, LabAssistant: 
    додає префікс до tab_nomer, якщо користувач ввів лише цифри.
    """
    
    list_display = ('tab_nomer',)
    
    def save_model(self, request, obj, form, change):
        # 1. Визначаємо префікс для поточної моделі
        model_class = obj.__class__
        prefix = ''
        if model_class == Doctor:
            prefix = 'DOC-'
        elif model_class == Personnel:
            prefix = 'MEDP-'
        elif model_class == LaboratoryAssistent:
            prefix = 'LAB-'
        
        # 2. Перевіряємо та додаємо префікс, якщо це числовий ввід без префікса
        tab_nomer_input = obj.tab_nomer
        
        # Перевіряємо, чи існує ввід і чи не починається він вже з нашого префікса
        if tab_nomer_input and prefix and not tab_nomer_input.startswith(prefix):
            
            # Якщо введений текст складається лише з цифр
            if tab_nomer_input.isdigit():
                
                # Додаємо префікс до числової частини
                obj.tab_nomer = f"{prefix}{tab_nomer_input}"
                
            # Якщо введений текст не є лише цифрами і не має префікса,
            # він зберігається як є (наприклад, "123-ABC" або просто "TEST")
        
        # Якщо префікс вже є (наприклад, DOC12345), або prefix порожній, зберігаємо без змін.
            
        super().save_model(request, obj, form, change)


# --- 3. Реєстрація моделей з кастомними Admin класами ---
# Ця частина залишається без змін

@admin.register(Doctor)
class DoctorAdmin(BasePersonnelAdmin):
    list_display = ('tab_nomer', 'user', 'stazh', 'specialization', 'Umovy_pryyomu')
    
@admin.register(Personnel)
class PersonnelAdmin(BasePersonnelAdmin):
    list_display = ('tab_nomer', 'user', 'stazh', 'department', 'position')

@admin.register(LaboratoryAssistent)
class LaboratoryAssistentAdmin(BasePersonnelAdmin):
    list_display = ('tab_nomer', 'user', 'stazh', 'specialization')
