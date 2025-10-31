from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.urls import reverse
from users_app.forms import UserLoginForm

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
  return render(request, 'users/reg.html')

def profile(request):
  return render(request, 'users/profile.html')

def logout(request):
  return render(request, 'users/logout.html')