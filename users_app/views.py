from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth
from django.urls import reverse
from users_app.forms import UserLoginForm, UserRegForm, ProfileForm

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
  if request.method == 'POST':
    form = ProfileForm(data=request.POST, instance=request.user, files=request.files)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('user:profile'))
  else:
    form = ProfileForm(instance=request.user)
  context = {'form': form}
  return render(request, 'users/profile.html', context)