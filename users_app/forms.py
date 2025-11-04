from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import CustomUser, Patient, Doctor, FamilyDoctor, LaboratoryAssistent, Personnel
from phonenumber_field.formfields import PhoneNumberField
from datetime import date, timedelta

class UserLoginForm(AuthenticationForm):
  username = forms.CharField()
  password = forms.CharField()
  # username = forms.CharField(
  #   label= 'Логін',
  #   widget=forms.TextInput(attrs={'autofocus': True,
  #                                 'placeholder': 'Введіть нік',
  #                                 'class': 'form-control'})
  #                                 )
  # password = forms.CharField(
  #   label= 'Пароль',
  #   widget=forms.PasswordInput(attrs={'placeholder': 'Введіть пароль',
  #                                     'class': 'form-control',})
  #                                     )
  class Meta:
    model = CustomUser
    fields = ['username', 'password']


class UserRegForm(UserCreationForm):
  password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
  password2 = forms.CharField(label='Повторіть пароль', widget=forms.PasswordInput())
  class Meta:
    model = CustomUser
    fields = ("first_name", "last_name", "username",
                  "email", "phone_number", "password1", "password2",)


class ProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("img", "first_name", "last_name",
                  "patronymic", "email", "phone_number",
                  )


class DoctorForm(forms.ModelForm):
  class Meta:
    model = Doctor
    fields = ("tab_nomer", "specialization", "stazh", "Umovy_pryyomu")


class LabAssistantForm(forms.ModelForm):
  class Meta:
    model = LaboratoryAssistent
    fields = ("tab_nomer", "specialization", "stazh")


class PersonnelForm(forms.ModelForm):
  class Meta:
    model = Personnel
    fields = ("tab_nomer", "stazh", "department", "position")


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ("date_of_birth", "sex")
        date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    def clean_date_of_birth(self):
        value = self.cleaned_data.get("date_of_birth")
        today = date.today()
        eighty_years_ago = today - timedelta(days=80*365.25)
        if value and value < eighty_years_ago:
            raise forms.ValidationError(f'Дане поле не приймає дати, менші за {eighty_years_ago}')
        elif value and value> date.today():
            raise forms.ValidationError(f'Дане поле не приймає дати, більші за {date.today()}' )
        return value
    

class FamilyDoctorForm(forms.ModelForm):
  class Meta:
    model = FamilyDoctor
    fields = '__all__'

  def clean(self):
    cleaned_data = super().clean()
    patient = cleaned_data.get("patient")
    doctor = cleaned_data.get("doctor")

    if self.instance.pk:
      # Якщо запис вже існує, виключити його з перевірки
      if FamilyDoctor.objects.filter(patient=patient).exclude(pk=self.instance.pk).exists():
        raise forms.ValidationError("Цей пацієнт вже має сімейного лікаря")
    else:
      # Якщо запис новий, виконати стандартну перевірку
      if FamilyDoctor.objects.filter(patient=patient).exists():
        raise forms.ValidationError("Цей пацієнт вже має сімейного лікаря")

    return cleaned_data