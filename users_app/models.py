from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser): 
  img = models.ImageField(upload_to='media/users_img', blank=True, null=True, verbose_name='Фото')
  email = models.EmailField(unique=True, verbose_name= 'Email')
  first_name = models.CharField(max_length=100, verbose_name= 'Iмя')
  last_name = models.CharField(max_length=100, verbose_name= 'Призвіще')
  patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name= 'По-батькові')
  phone_number = PhoneNumberField(unique=True, verbose_name= 'Номер телефону')
  class Meta:
    db_table = 'Users'
    verbose_name = 'Користувача'
    verbose_name_plural = 'Користувачі'
  def __str__(self):
    return f"{self.id}. Логін: {self.username}"


class Doctor(models.Model):
  tab_nomer = models.CharField(max_length=20, primary_key=True,verbose_name="Табельний номер")
  user = models.OneToOneField("users_app.CustomUser", verbose_name="ID користувача", on_delete=models.CASCADE)
  stazh = models.CharField(max_length=50, blank=True, null=True, verbose_name='Cтаж')
  specialization = models.CharField(max_length=100,verbose_name='Спеціалізація')
  Umovy_pryyomu = models.CharField(max_length=250, blank=True, null=True, verbose_name='Умови прийому')    
  class Meta:
    db_table = 'Doctor'
    verbose_name = 'Лікаря'
    verbose_name_plural = 'Лікарі'
  def __str__(self):
    return self.tab_nomer


class Personnel(models.Model):
  tab_nomer = models.CharField(max_length=20, primary_key=True,verbose_name="Табельний номер")
  user = models.OneToOneField("users_app.CustomUser", verbose_name="ID користувача", on_delete=models.CASCADE)
  stazh = models.CharField(max_length=50, blank=True, null=True, verbose_name='Cтаж')
  department = models.CharField(max_length=100,verbose_name='Відділення')
  position = models.CharField(max_length=250, blank=True, null=True, verbose_name='Посада')    
  class Meta:
    db_table = 'MedPersonnel'
    verbose_name = 'Мед.персонал'
    verbose_name_plural = 'Мед.персонал'
  def __str__(self):
    return self.tab_nomer


class LaboratoryAssistent(models.Model):
  tab_nomer = models.CharField(max_length=20, primary_key=True,verbose_name="Табельний номер")
  user = models.OneToOneField("users_app.CustomUser", verbose_name="ID користувача", on_delete=models.CASCADE)
  stazh = models.CharField(max_length=50, blank=True, null=True, verbose_name='Cтаж')
  specialization = models.CharField(max_length=100,verbose_name='Спеціалізація')
  class Meta:
    db_table = 'LabAssistent'
    verbose_name = 'Асистента'
    verbose_name_plural = 'Лаб.Асистенти'
  def __str__(self):
    return self.tab_nomer


class Patient(models.Model):
  user = models.OneToOneField("users_app.CustomUser", verbose_name="ID користувача", on_delete=models.CASCADE)
  SEX = [
    ('Ч','Чоловік'),
    ('Ж','Жінка'),]
  sex = models.CharField(blank=True, null=True, max_length=1, choices=SEX, verbose_name='Cтать')
  date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата народження')
  id_doctor = models.ManyToManyField("users_app.Doctor", 
                                        through='FamilyDoctor')
  class Meta:
    db_table = 'Patient'
    verbose_name = 'Пацієнта'
    verbose_name_plural = 'Пацієнти'
  def __str__(self):
    return f"{self.user}"


class FamilyDoctor(models.Model):
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Пацієнт')
  doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,verbose_name='Лікар')
  class Meta:
    db_table = 'FamilyDoctor'
    verbose_name = 'Сімейного лікаря'
    verbose_name_plural = 'Сімейні лікарі'
    unique_together = ('patient', 'doctor')
  def __str__(self):
    return f"{self.doctor} - {self.patient}"

