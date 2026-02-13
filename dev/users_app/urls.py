from django.urls import path
from users_app import views

app_name = 'users_app'
urlpatterns = [
    path('login/',views.login, name='login'),#mysite.com/user/registration
    path('registration/',views.registration, name='registration'),#mysite.com/user/registration
    path('profile/',views.profile, name='profile'),#mysite.com/user/profile
    path('logout/',views.logout, name='logout'),#mysite.com/user/logout
]
