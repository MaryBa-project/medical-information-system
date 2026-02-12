from django.db import models
from django.forms import ValidationError

STATUS_CHOICES = [
    ('N', 'Активне'),
    ('C', 'Анульовано'),]

class MedReferral(models.Model):
  doctor = models.ForeignKey('users_app.Doctor', on_delete=models.PROTECT, verbose_name='ID лікаря')
  medcard = models.ForeignKey('cards_app.MedCards', on_delete=models.CASCADE, verbose_name='Номер медичної карти')
  type_analys = models.ForeignKey('TypeAnalysis', on_delete=models.PROTECT, verbose_name='ID типу аналізу')
  creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення направлення')
  coment = models.TextField(max_length=500, verbose_name='Коментар')
  status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N',
        verbose_name='Статус направлення'
    )
  class Meta:
    db_table = 'MedReferral'
    verbose_name = 'Направлення'
    verbose_name_plural = 'Направлення'
  def __str__(self):
    return f'{self.id}'
  def display_id(self):
    return f'{self.id:03}'


class TypeAnalysis(models.Model):
  name = models.CharField(max_length=100, verbose_name='Назва аналізу')
  description = models.TextField(max_length=500, blank=True, null=True, verbose_name='Опис аналізу')
  class Meta:
    db_table = 'TypeAnalys'
    verbose_name = 'Тип аналізу'
    verbose_name_plural = 'Типи аналізів'
  def __str__(self):
    return f'{self.id} - {self.name}'


class TemplateParameter(models.Model):
  name = models.CharField(max_length=100, verbose_name='Назва параметру')
  unit_of_measurement = models.CharField(max_length=20, verbose_name='Одиниці вимірювання')
  normal_min = models.DecimalField(max_digits=7,decimal_places=3, blank=True, null=True, verbose_name='Мінімально допустиме значення')
  normal_max = models.DecimalField(max_digits=7,decimal_places=3, blank=True, null=True, verbose_name='Максимально допустиме значення')
  type_analys = models.ForeignKey('TypeAnalysis', on_delete=models.CASCADE, verbose_name='ID типу аналізу')
  class Meta:
    db_table = 'TemplateParameter'
    verbose_name = 'Шаблон параметру'
    verbose_name_plural = 'Шаблони параметрів'
    unique_together = ('name', 'type_analys')
  def clean(self):
    super().clean()
    if self.normal_max <= self.normal_min:
      raise ValidationError({
        'normal_max': 'Максимальне значення має бути більшим за мінімальне.'})
  def __str__(self):
    return f'{self.id} - {self.name}'


class ResultParameter(models.Model):
  value = models.DecimalField(max_digits=6,decimal_places=3, verbose_name='Результат')
  unit_of_measurement = models.CharField(max_length=20, blank=True, null=True, verbose_name='Одиниці вимірювання')
  coment = models.CharField(max_length=100, verbose_name='Коментар')
  template = models.ForeignKey('TemplateParameter', on_delete=models.CASCADE, verbose_name='ID шаблону аналізу')
  result_analys = models.ForeignKey('ResultAnalysis', on_delete=models.CASCADE, verbose_name='ID результатів аналізів')
  class Meta:
    db_table = 'ResultParameter'
    verbose_name = 'Результат параметру'
    verbose_name_plural = 'Результати параметрів'
  def __str__(self):
    return f'{self.id}'


class ResultAnalysis(models.Model):
  medcard = models.ForeignKey('cards_app.MedCards', on_delete=models.CASCADE, verbose_name='Номер медичної карти')
  referral = models.OneToOneField('MedReferral', on_delete=models.PROTECT, verbose_name='ID направлення')
  lab_assistent = models.ForeignKey('users_app.LaboratoryAssistent', on_delete=models.PROTECT, verbose_name='ІD лаборанта')
  providing_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заповнення виcновку')
  report = models.TextField(max_length=500, verbose_name='Висновок')
  class Meta:
    db_table = 'ResultAnalys'
    verbose_name = 'Результат аналізу'
    verbose_name_plural = 'Результати аналізів'
  def __str__(self):
    return f'{self.id}'
  def display_id(self):
    return f'{self.id:03}'