from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from cards_app.models import CardVaccine, IndividualMarks, MedCards, SignalMarks
from laboratory_app.models import MedReferral, ResultAnalysis
from users_app.models import Doctor, Patient, Personnel



################ Мед персонал ##############
@login_required
def all_cards(request):
    user = request.user
    user_groups = request.user.groups.values_list('name', flat=True)
        # Отримуємо об'єкт лікаря, який відповідає поточному користувачу
    doctor = Doctor.objects.filter(user=user).first()
    patients_with_cards = Patient.objects.select_related('user').prefetch_related('medcards').filter(medcards__isnull=False).distinct()
    
    if not any(group in ["ЛІКАРІ", "МЕД.ПЕРСОНАЛ"] for group in user_groups):
        raise Http404("Сторінка не знайдена")
    
    if doctor:
        card_active_redact = patients_with_cards.filter(id_doctor=doctor)
    else:
        # Для персоналу чи інших користувачів — редагування заборонене
        card_active_redact = Patient.objects.none()
    context = {
        'user_groups': list(user_groups),
        'patients_with_cards': patients_with_cards,
        'user': request.user,
        'doctor': doctor,
        'card_active_redact': card_active_redact,
    }
    return render(request, 'cards/all_cards.html', context)


@login_required
def not_card(request):
    return render(request, 'cards_app/not_card.html')

@login_required
def index(request, card_id):
  return render(request, 'cards/index_card.html')

@login_required
def vaccine(request, card_id):
  return render(request, 'cards/vaccine.html')

@login_required
def med_referral(request, card_id):
  return render(request, 'cards/med_referral.html')

@login_required
def result_analysis(request, card_id):
  return render(request, 'cards/result_analysis.html')


################ Пацієнти ##############


@login_required
def card_profile(request):
  user = request.user
  patient = get_object_or_404(Patient, user=user)
  card = get_object_or_404(MedCards.objects.select_related('patient', 
                                            'patient__user', 'doctor', 'doctor__user').prefetch_related('individualmarks_set'),patient=patient)
  individual_marks = IndividualMarks.objects.filter(medcard=card)
  context = {
                'user': user,
                'patient': patient,
                'card': card,
                'individual_marks' : individual_marks
            }
  return render(request, 'cards/card_profile.html', context)


@login_required
def vaccine_profile(request):
    user = request.user
    patient = get_object_or_404(Patient, user=user) 
    card = MedCards.objects.select_related('patient', 'patient__user','doctor').filter(patient=patient).first() 
    card_vaccinations = []
    
    # 4. Отримуємо щеплення ТІЛЬКИ, якщо картка існує
    if card:
        card_vaccinations = CardVaccine.objects.filter(medcard=card)

    context = {
        'user': user,
        'patient': patient,
        'card': card, # Тут буде об'єкт АБО None
        'card_vaccinations': card_vaccinations,
    }
    return render(request, 'cards/vaccine_profile.html', context)


@login_required
def referral_profile(request):
  user = request.user
  patient = get_object_or_404(Patient, user=user) 
  card = MedCards.objects.select_related('patient', 'patient__user','doctor').filter(patient=patient).first() 
  card_referral = []
  if card:
    card_referral = MedReferral.objects.filter(medcard=card)
  
  context = {
        'user': user,
        'patient': patient,
        'card': card, # Тут буде об'єкт АБО None
        'card_referral': card_referral,
    }
  return render(request, 'cards/referral_profile.html', context)




@login_required
def result_analysis_profile(request):
  user = request.user
  patient = get_object_or_404(Patient, user=user) 
  card = MedCards.objects.select_related('patient', 'patient__user','doctor').filter(patient=patient).first() 
  card_analysis = []
  if card:
    card_analysis = ResultAnalysis.objects.filter(medcard=card)
  
  context = {
        'user': user,
        'patient': patient,
        'card': card, # Тут буде об'єкт АБО None
        'card_analysis': card_analysis,
    }
  return render(request, 'cards/result_analysis_profile.html', context)
