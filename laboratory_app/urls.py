from django.urls import path
from laboratory_app import views

app_name = 'laboratory_app'
urlpatterns = [

  ###### ЛАБОРАНТИ #######
  path('lab-journal/', views.lab_journal, name='lab_journal'),
  path('lab-norms/', views.lab_norms, name='lab_norms'), 
]