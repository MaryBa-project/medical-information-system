from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from cards_app.forms import CardVaccineForm, IndividualMarksFormSet, MedReferralForm, ReferralAddForm
from cards_app.models import CardVaccine, IndividualMarks, MedCards
from laboratory_app.models import MedReferral, ResultAnalysis
from users_app.models import Doctor, Patient



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
        'card_active_redact': card_active_redact}
    return render(request, 'cards/all_cards.html', context)


@login_required
def not_card(request):
    return render(request, 'cards_app/not_card.html')



### --Головна сторінка карти та сигнальні позначки-- ###
@login_required
def index(request, card_id):
    user_groups = request.user.groups.values_list('name', flat=True)
    if "ЛАБОРАНТИ" in user_groups:
        raise Http404("Сторінка не знайдена")
    card = get_object_or_404(MedCards.objects.select_related('patient', 
                                            'patient__user', 'doctor', 'doctor__user').prefetch_related('individualmarks_set'),  id=card_id)
    individual_marks = IndividualMarks.objects.filter(medcard=card)
    current_user = request.user
    doctor = card.doctor.user if card.doctor else None
    can_edit = doctor == current_user
    context = {
        'card': card,
        'can_edit': can_edit,
        'individual_marks': individual_marks}
    return render(request, 'cards/card_profile.html', context)


@login_required
def edit_mark(request, card_id):
    user_groups = request.user.groups.values_list('name', flat=True)
    if not "ЛІКАРІ" in user_groups:
        raise Http404("Сторінка не знайдена")
    # 1. Отримуємо конкретну медкарту за id
    card = get_object_or_404(
        MedCards.objects.prefetch_related('individualmarks_set'), id=card_id)
    # 2. Обробка POST-запиту (збереження форми)
    if request.method == 'POST':
        # Створюємо FormSet, прив'язуючи дані з POST та instance
        formset = IndividualMarksFormSet(request.POST, instance=card)
        if formset.is_valid():
            formset.save()
            return redirect('card:index', card_id=card.id) 
    # Обробка GET-запиту (відображення форми)
    else:
        formset = IndividualMarksFormSet(instance=card)
    context = {
        'card': card,
        'formset': formset}
    return render(request, 'cards/edit_signal_marks.html', context)



### --Вакцинація-- ###
@login_required
def vaccine(request, card_id):
    user_groups = request.user.groups.values_list('name', flat=True)
    if "ЛАБОРАНТИ" in user_groups:
        raise Http404("Сторінка не знайдена")
     # Отримуємо медичну картку за її ID з вибіркою пов'язаних об'єктів (пацієнт, користувач пацієнта, лікар, користувач лікаря)
    card = get_object_or_404(MedCards.objects.select_related('patient', 'patient__user', 'doctor', 'doctor__user'), id=card_id)
    card_vaccinations = CardVaccine.objects.filter(medcard=card).order_by('id') # Отримуємо всі вакцинації, пов'язані з цією медичною карткою
    current_user = request.user
    # Отримуємо користувача лікаря, якщо лікар прив'язаний до медичної картки, інакше None
    doctor = card.doctor.user if card.doctor else None
    is_medical_staff = "МЕД.ПЕРСОНАЛ" in user_groups
    # Перевіряємо, чи поточний користувач є лікарем, прив'язаним до медичної картки
    can_edit = doctor == current_user or is_medical_staff
    context = {
        'card': card,
        'card_vaccinations': card_vaccinations,
        'can_edit': can_edit}
    return render(request, 'cards/vaccine_profile.html', context)


@login_required
def add_vaccine(request, card_id):
    card = get_object_or_404(MedCards, id=card_id)
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    is_medical_staff = "МЕД.ПЕРСОНАЛ" in user_groups
    is_assigned_doctor = "ЛІКАРІ" in user_groups and card.doctor and card.doctor.user == user
    has_access = is_medical_staff or is_assigned_doctor
    if not has_access:
        raise Http404("Сторінка не знайдена")
    if request.method == 'POST':
        form = CardVaccineForm(request.POST)
        if form.is_valid():
            card_vaccine = form.save(commit=False) # Створення екземпляру без збереження
            card_vaccine.medcard = card  # Присвоюємо медичну карту
            card_vaccine.save()
            return HttpResponseRedirect(reverse('card:vaccine', args=[card.display_id()]))
    else:
        form = CardVaccineForm()
    context = {
    'form': form,
    'card': card,
    'has_access': has_access}
    return render(request, 'cards/add_vaccine.html', context)


@login_required
def edit_vaccine(request, vaccine_id):
    vaccine = get_object_or_404(CardVaccine, id=vaccine_id)
    card = vaccine.medcard  # якщо треба для шаблону

    if request.method == 'POST':
        form = CardVaccineForm(request.POST, instance=vaccine)
        if form.is_valid():
            form.save()
            return redirect('card:vaccine', card_id=card.display_id())
    else:
        form = CardVaccineForm(instance=vaccine)
    context = {
        'form': form,
        'card': card}
    return render(request, 'cards/edit_vaccine.html', context)



### --Направлення-- ###

# Перегляд без прив'язки до карти
@login_required
def lab_journal(request):
    user = request.user
    user_groups = request.user.groups.values_list('name', flat=True)
    
    # 1. Перевірка на групу "ЛАБОРАНТИ"
    if "ЛАБОРАНТИ" in user_groups:
        card_referral = MedReferral.objects.exclude(status='C')
        context = {
            'user': user,
            'card_referral': card_referral,
            }
        return render(request, 'laboratory/lab_journal.html', context)
    elif "ЛІКАРІ" in user_groups:
        doctor = get_object_or_404(Doctor, user=request.user)
        card_referral = MedReferral.objects.filter(doctor=doctor) # <--- ВИКОРИСТОВУЄМО user (який є request.user)
        context = {
            'user': user,
            'doctor':doctor,
            'card_referral': card_referral,
        }
        return render(request, 'laboratory/lab_journal.html', context)
    return HttpResponseForbidden("У вас немає доступу до цієї сторінки")


# Перегляд з прив'язкою до карти
@login_required
def med_referral(request, card_id):
    user = request.user
    user_groups = request.user.groups.values_list('name', flat=True)
    
    # 1. Перевірка на групу "ЛІКАРІ" або "МЕД.ПЕРСОНАЛ"
    if "ЛІКАРІ" in user_groups or "МЕД.ПЕРСОНАЛ" in user_groups:
        card = get_object_or_404(MedCards, id=card_id)
        card_referral = MedReferral.objects.filter(medcard=card)
        
        context = {
            'user': user,
            'card_referral': card_referral,
            'card': card,
        }
        return render(request, 'cards/referral_profile.html', context)
        
    # 2. Якщо користувач не належить до груп, які мають доступ
    return HttpResponseForbidden("У вас немає доступу до цієї сторінки")


@login_required
def add_referral(request, card_id):
    card = get_object_or_404(MedCards, id=card_id)
    user = request.user

    # Перевірка групи лікарів
    if "ЛІКАРІ" not in user.groups.values_list('name', flat=True):
        return HttpResponseForbidden("У вас немає доступу до цієї сторінки")

    if request.method == 'POST':
        form = ReferralAddForm(request.POST)
        if form.is_valid():
            referral = form.save(commit=False)
            referral.medcard = card
            referral.doctor = get_object_or_404(Doctor, user=user)
            referral.status = 'N'  # Активне при створенні
            referral.save()
            return redirect('card:referral_card', card_id=card.display_id())
    else:
        form = ReferralAddForm()

    return render(request, 'cards/add_referral.html', {'form': form, 'card': card})




@login_required
def edit_referral(request, referral_id):
    referral = get_object_or_404(MedReferral, id=referral_id)
    card = referral.medcard
    if not (
        referral.doctor.user == request.user or 
        card.doctor.user == request.user
    ):
        return HttpResponseForbidden("У вас немає доступу до редагування цього направлення")

    if request.method == 'POST':
        form = MedReferralForm(request.POST, instance=referral)
        if form.is_valid():
            form.save()
            return redirect('card:referral_card', card_id=card.display_id())
    else:
        form = MedReferralForm(instance=referral)

    return render(request, 'cards/edit_referral.html', {
        'form': form,
        'referral': referral,
        'card': card,
    })











### --Аналізи-- ###
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


@login_required
def result_id_profile(request, card_analysis_id):
    user = request.user
    patient = get_object_or_404(Patient, user=user)
    card_analysis = get_object_or_404(ResultAnalysis, id=card_analysis_id, medcard__patient=patient)

    card = card_analysis.medcard

    context = {
        'user': user,
        'patient': patient,
        'card': card,
        'card_analysis': card_analysis,
    }
    return render(request, 'cards/result_analysis_view.html', context)