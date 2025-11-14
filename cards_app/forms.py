from django import forms
from .models import IndividualMarks
from django.forms import inlineformset_factory
from .models import MedCards

class IndividualMarkForm(forms.ModelForm):
    class Meta:
        model = IndividualMarks
        fields = ['value']
        # Якщо ви хочете відображати назву позначки (SignalMarks) як приховане поле, 
        # ви можете додати 'signal_mark', але краще це робити через FormSet.


IndividualMarksFormSet = inlineformset_factory(
    parent_model=MedCards, 
    model=IndividualMarks, 
    form=IndividualMarkForm, # Використовуємо нашу спеціальну форму
    fields=['value'],        # Поля, які ми хочемо редагувати
    extra=0,                 # Важливо: не дозволяємо додавати нові порожні позначки
    can_delete=False         # Не дозволяємо видаляти існуючі позначки
)
