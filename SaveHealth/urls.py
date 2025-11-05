"""
URL configuration for SaveHealth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from SaveHealth import settings
from django.conf.urls.static import static

urlpatterns = [
    path('root/', admin.site.urls), #mysite.com/root
    path('', include('public_app.urls', namespace='public')), # з'єднання з public_app
    path('user/', include('users_app.urls', namespace='user')), # з'єднання з users_app
    path('profile/med_card/', include('cards_app.urls', namespace='card')), # з'єднання з cards_app
    path('profile/laboratory/', include('laboratory_app.urls', namespace='laboratory')) # з'єднання з laboratory_app

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)