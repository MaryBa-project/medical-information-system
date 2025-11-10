from django.contrib import admin
from .models import MedCards, SignalMarks, IndividualMarks, Vaccination, CardVaccine, DoctorExamination, Personnel_MedCard

# @admin.register(MedCards)
# сlass MedCardsAdmin(admin.ModelAdmin):
#   prepopulated_fields = {'slug': ('id'),}


# class MedCardsAdmin(admin.ModelAdmin):
#   readonly_fields = ('patient', 'doctor')
#   list_display = ('id','patient', 'doctor', 'dispensary_group', 'registration_date', 'deregistration_date')


# Адмінка для MedCards
class MedCardsAdmin(admin.ModelAdmin):
  list_display = ('id', 'patient', 'doctor', 'dispensary_group', 'registration_date')
#     search_fields = ('patient__full_name', 'doctor__last_name', 'slug') 
  readonly_fields = ('registration_date','patient', 'doctor',) 
#     inlines = [IndividualMarksInline, DoctorExaminationInline]
admin.site.register(MedCards, MedCardsAdmin)



admin.site.register(IndividualMarks)
admin.site.register(SignalMarks)
admin.site.register(Vaccination)
admin.site.register(CardVaccine) 
admin.site.register(DoctorExamination)
admin.site.register(Personnel_MedCard)

