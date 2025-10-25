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


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Doctor)
admin.site.register(Personnel)
admin.site.register(Patient)
admin.site.register(LaboratoryAssistent)
admin.site.register(FamilyDoctor)
