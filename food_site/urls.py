"""
URL configuration for food_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import (views as auth_views)
from main.views import index_page, logout_view, home_page, profile, create_menu, create_recipe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', logout_view),
    path('home/', home_page, name = 'home'),
    path('profile/', profile, name = 'profile'),
    path('menu/', create_menu, name = 'menu'),
    path('recipe/', create_recipe, name = 'recipe'),
    path("accounts/", include("django_registration.backends.one_step.urls")),
    path("accounts/", include("django.contrib.auth.urls"))
]
