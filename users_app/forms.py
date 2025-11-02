from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users_app.models import CustomUser

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