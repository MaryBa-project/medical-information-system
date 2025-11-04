from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth
from django.urls import reverse
from users_app.forms import ProfileForm, UserLoginForm, UserRegForm, PatientForm, DoctorForm, LabAssistantForm, PersonnelForm
from users_app.models import Doctor, Patient, LaboratoryAssistent, Personnel

def login(request):
  if request.method == 'POST':
    form = UserLoginForm(data=request.POST)  # екземпляр форми логіну, що передає дані, які користувач ввів
    if form.is_valid():
      username = request.POST['username'] ## зі словника добуваєм username & password
      password = request.POST['password']
      user = auth.authenticate(username=username, password=password) ## чи є такий користувач??
      if user:
        auth.login(request, user)

      if request.POST.get('next', None):
          return HttpResponseRedirect(request.POST.get('next'))
      return HttpResponseRedirect(reverse('user:profile'))
  else:
    form = UserLoginForm()
  context = {'form': form}
  return render(request, 'users/login.html', context)


def registration(request):
  if request.method == 'POST':
    form = UserRegForm(data=request.POST)  # екземпляр форми логіну, що передає дані, які користувач ввів
    if form.is_valid():
      form.save()
      # user = form.instance - екземпляр форми
      # auth.login(request, user) - авто логін
      # return HttpResponseRedirect(reverse('user:profile'))
      return HttpResponseRedirect(reverse('user:login'))
  else:
    form = UserRegForm()
  context = {'form': form}
  return render(request, 'users/reg.html', context)


@login_required
def logout(request):
  auth.logout(request)
  return redirect(reverse('public:index'))


@login_required
def profile(request):
    user = request.user # поточний користувач 
    user_groups = user.groups.values_list('name', flat=True) # список груп
    
    form = ProfileForm(instance=user) # отримання даних з форми профілю
    patient_form = None ## змінні з незаповненими формами
    doctor_form = None
    assistant_form = None
    personnel_form = None

    if request.method == 'POST':
      form = ProfileForm(data=request.POST, instance=user, files=request.FILES) # Створення форми з даними з POST-запиту
        
      if 'ПАЦІЄНТИ' in user_groups:
        patient_instance, created = Patient.objects.get_or_create(user=user) # Отримання або створення об'єкту пацієнта для користувача
        patient_form = PatientForm(request.POST, instance=patient_instance, prefix='p') # Створення форми пацієнта з даними з POST-запиту

      if 'ЛІКАРІ' in user_groups:
        try:
          doctor_instance = Doctor.objects.get(user=user) # Спроба отримати об'єкт лікаря для користувача
          doctor_form = DoctorForm(request.POST, instance=doctor_instance, prefix='d') # Створення форми лікаря з даними з POST-запиту
        except Doctor.DoesNotExist: # Якщо об'єкт лікаря не знайдено
          doctor_form = None
        
      if 'МЕД.ПЕРСОНАЛ' in user_groups:
        try:
          personnel_instance =  Personnel.objects.get(user=user) # Спроба отримати об'єкт лікаря для користувача
          personnel_form = PersonnelForm(request.POST, instance=personnel_instance, prefix='med-p') # Створення форми лікаря з даними з POST-запиту
        except Personnel.DoesNotExist: # Якщо об'єкт лікаря не знайдено
          personnel_form = None

      if 'ЛАБОРАНТИ' in user_groups:
        try:
          assistant_instance =  LaboratoryAssistent.objects.get(user=user) # Спроба отримати об'єкт лікаря для користувача
          assistant_form = LabAssistantForm(request.POST, instance=assistant_instance, prefix='lab') # Створення форми лікаря з даними з POST-запиту
        except LaboratoryAssistent.DoesNotExist: # Якщо об'єкт лікаря не знайдено
          assistant_form = None

      if form.is_valid() and (patient_form is None or patient_form.is_valid()) and \
        (doctor_form is None or doctor_form.is_valid()) and \
        (personnel_form is None or personnel_form.is_valid()) and \
        (assistant_form is None or assistant_form.is_valid()):
          form.save()
          if patient_form:
            patient_form.save()
          if doctor_form:
            doctor_form.save()
          if personnel_form:
            personnel_form.save()
          if assistant_form:
            assistant_form.save()  
            return HttpResponseRedirect(reverse('user:profile'))
          
    else:
      if 'ПАЦІЄНТИ' in user_groups:
        patient_instance, created = Patient.objects.get_or_create(user=user) # Отримання або створення об'єкту пацієнта для користувача
        patient_form = PatientForm(instance=patient_instance, prefix='p') # Створення форми пацієнта з даними користувача

      if 'ЛІКАРІ' in user_groups:
        try:
          doctor_instance = Doctor.objects.get(user=user) # Спроба отримати об'єкт лікаря для користувача
          doctor_form = DoctorForm(instance=doctor_instance, prefix='d')  # Створення форми лікаря з даними користувача
        except Doctor.DoesNotExist:
          doctor_form = None
        
      if 'МЕД.ПЕРСОНАЛ' in user_groups:
        try:
          personnel_instance =  Personnel.objects.get(user=user)
          personnel_form = PersonnelForm(instance=personnel_instance, prefix='med-p')
        except Personnel.DoesNotExist: 
          personnel_form = None

      if 'ЛАБОРАНТИ' in user_groups:
        try:
          assistant_instance =  LaboratoryAssistent.objects.get(user=user) # Спроба отримати об'єкт лікаря для користувача
          assistant_form = LabAssistantForm(instance=assistant_instance, prefix='lab') # Створення форми лікаря з даними з POST-запиту
        except LaboratoryAssistent.DoesNotExist: # Якщо об'єкт лікаря не знайдено
          assistant_form = None


    context = {
        'form': form,
        'user_groups': list(user_groups),
        'patient_form': patient_form,
        'doctor_form': doctor_form,
        'assistant_form': assistant_form,
        'personnel_form': personnel_form,
    }
    return render(request, 'users/profile.html', context)