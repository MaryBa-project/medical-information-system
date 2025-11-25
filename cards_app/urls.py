from django.urls import path
from cards_app import views

app_name = 'cards_app'
urlpatterns = [

  
  ###### ЛІКАРІ #######
    path('all_cards/',views.all_cards, name='all_cards'),
    path('<int:card_id>/',views.index, name='index'), # med-card/00005/
    path('edit-mark/<int:card_id>/',views.edit_mark, name='edit_mark'),
    path('vaccine/<int:card_id>/',views.vaccine, name='vaccine'),
    path('add-vaccine/<int:card_id>/', views.add_vaccine, name='add_vaccine'),
    path('edit-vaccine/<int:vaccine_id>/', views.edit_vaccine, name='edit_vaccine'),
    path("med-referral_staff/", views.lab_journal, name="journal_referral"),
    path('med-referral/<int:card_id>/',views.med_referral, name='referral_card'),
    path('edit-referral/<int:referral_id>/',views.edit_referral, name='edit_referral'),
    path('add-referral/<int:card_id>/',views.add_referral, name='add_referral'),
    path('result-analysis/<int:card_id>/',views.result_analysis, name='result_analysis'),
  
  ###### ПАЦІЄНТИ #######
    path('', views.card_profile, name='card_profile'), # med-card/card-profile/
    path('vaccine/', views.vaccine_profile, name='vaccine_profile'), 
    path('referral/', views.referral_profile, name='referral_profile'), 
    path('result-analysis/', views.result_analysis_profile, name='result_analysis_profile'), 
    path('result-card/<int:card_analysis_id>/', views.result_id_profile, name='result_id_profile'),

]