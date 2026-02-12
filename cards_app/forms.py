from datetime import date, timedelta
from django.core.validators import MinLengthValidator
from django import forms
from django.utils import timezone

from laboratory_app.models import MedReferral, TypeAnalysis
from .models import CardVaccine, IndividualMarks, Vaccination
from django.forms import inlineformset_factory
from .models import MedCards

class IndividualMarkForm(forms.ModelForm):
    class Meta:
        model = IndividualMarks
        fields = ['value']

IndividualMarksFormSet = inlineformset_factory(
    parent_model=MedCards, 
    model=IndividualMarks, 
    form=IndividualMarkForm, # Використовуємо нашу спеціальну форму
    fields=['value'],        # Поля, які ми хочемо редагувати
    extra=0,                 # Важливо: не дозволяємо додавати нові порожні позначки
    can_delete=False         # Не дозволяємо видаляти існуючі позначки
)


class CardVaccineForm(forms.ModelForm):
    class Meta:
        model = CardVaccine
        fields = ['vaccination','product_series','reaction','contraindication','date_vaccine']


    vaccination = forms.ModelChoiceField(
    queryset=Vaccination.objects.all(),
    widget=forms.Select(attrs={
        'class': 'form-select',
        'id': 'id_vaccination',
    })
)

    contraindication = forms.CharField(widget=forms.Textarea())
    product_series = forms.CharField(validators=[MinLengthValidator(5)])
    date_vaccine = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    
        # ---- Перевірка дати створення (редагування) ----
    def clean(self):
        cleaned_data = super().clean()

        if self.instance.pk:
            created_date = self.instance.date_vaccine     # це date
            now = timezone.now().date()                  # теж date

            days_passed = (now - created_date).days      # різниця в днях
            hours_passed = days_passed * 24              # переводимо в години

            if hours_passed > 48:
                raise forms.ValidationError(
                    "Редагування цього запису заборонено — минуло більше 48 годин від моменту створення."
                )

        return cleaned_data

    
    def clean_date_vaccine(self):
        value = self.cleaned_data.get("date_vaccine")
        today = date.today()
        week_ago = today - timedelta(days=7)
        if value and value < week_ago:
            raise forms.ValidationError(f'Дане поле не приймає дати, менші за {week_ago}')
        elif value and value > date.today():
            raise forms.ValidationError(f'Дане поле не приймає дати, більші за {date.today()}' )
        return value


class MedReferralForm(forms.ModelForm):
    
    class Meta:
        model = MedReferral
        fields = [ 'coment', 'status']


class ReferralAddForm(forms.ModelForm):
    # Оголошуємо поле типу аналізу без класів Bootstrap
    type_analys = forms.ModelChoiceField(
        queryset=TypeAnalysis.objects.all(),
        empty_label="Виберіть тип аналізу",
        widget=forms.Select()
    )

    class Meta:
        model = MedReferral
        fields = ['type_analys', 'coment']  # status і creation_date не редагуються
        # widgets більше не потрібні, бо поле вже вказане вище