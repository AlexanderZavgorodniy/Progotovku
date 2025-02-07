import datetime

from django.contrib.auth import logout, login
from django.shortcuts import render

from main.forms import RegistrationForm
from main.models import Dish

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator



def index_page(request):
    return redirect('home')



def logout_view(request):
    logout(request)
    return redirect('/')


def home_page(request):
    context = {}
    return render(request, 'home.html', context)


def profile(request):
    context = {}
    return render(request, 'profile.html', context)


def create_menu(request):
    context = {}
    return render(request, 'menu.html', context)


def create_recipe(request):
    context = {}
    return render(request, 'recipe.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя
            login(request, user)  # Автоматически авторизуем пользователя после регистрации
            #messages.success(request, "Регистрация успешно завершена!")
            return redirect('home')  # Перенаправляем на главную страницу
        else:
            pass
           # messages.error(request, "Ошибка регистрации. Пожалуйста, исправьте данные.")
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def dish(request, id):
    context = {}
    dish = Dish.objects.get(id = id)
    context['dish'] = dish
    return render(request, 'dish.html', context)


def dish_all(request):
    context = {}
    dish_list = Dish.objects.all()
    paginator = Paginator(dish_list, 9)  # 9 карточек на страницу

    page_number = request.GET.get('page')
    context['dishes'] = paginator.get_page(page_number)
    return render(request, 'dish_all.html', context)
