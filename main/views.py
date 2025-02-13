import datetime
from itertools import combinations
import random

from django.contrib.auth import logout, login
from django.db.models import F
from django.db.models.functions import Abs
from django.shortcuts import render

from main.forms import RegistrationForm
from main.models import Dish, ProfileData

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from .utils import get_calories_declension



def index_page(request):
    return redirect('home')



def logout_view(request):
    logout(request)
    return redirect('/')


def home_page(request):
    context = {}
    return render(request, 'home.html', context)


@login_required
def profile(request):
    context = {}

    try:
        # Пытаемся получить объект ProfileData для текущего пользователя
        profile_data = ProfileData.objects.get(user=request.user)
        context["calories"] = str(profile_data.calories_num) + " " + get_calories_declension(profile_data.calories_num)

    except ProfileData.DoesNotExist:
        # Если объект ProfileData не существует, добавляем предупреждение в контекст
        context['warning'] = "Вы не указали ежедневное количество калорий"
        profile_data = None
    if request.method == "POST":
        calories_num = request.POST.get('calories_num')
        if calories_num and calories_num.isdigit():  # Проверяем, что введено число
            calories_num = int(calories_num)
            if profile_data:
                profile_data.calories_num = calories_num
                profile_data.save()
            else:
                ProfileData.objects.create(user=request.user, calories_num=calories_num)
            return redirect('profile')  # Перенаправление после успешного сохранения

    return render(request, 'profile.html', context)


@login_required
def create_menu(request):
    context = {}

    try:
        # Получаем объект ProfileData текущего пользователя
        profile_data = ProfileData.objects.get(user=request.user)
        target_calories = profile_data.calories_num

        # Получаем все доступные блюда
        all_dishes = list(Dish.objects.all())

        if len(all_dishes) < 3:
            context['error'] = "Недостаточно блюд для создания меню."
            return render(request, 'menu.html', context)

        # Генерируем все возможные комбинации из трех блюд
        dish_combinations = list(combinations(all_dishes, 3))

        # Сортируем комбинации по близости их суммы калорий к target_calories
        sorted_combinations = sorted(
            dish_combinations,
            key=lambda combo: abs(sum(dish.calories for dish in combo) - target_calories)
        )

        # Берем первые 10 лучших комбинаций
        top_combinations = sorted_combinations[:10]

        if not top_combinations:
            context['error'] = "Не найдено подходящих комбинаций блюд."
            return render(request, 'menu.html', context)

        # Выбираем одну случайную комбинацию из первых 10
        closest_combination = random.choice(top_combinations)

        # Вычисляем общую сумму калорий для выбранной комбинации
        total_calories = sum(dish.calories for dish in closest_combination)

        context['closest_dishes'] = closest_combination
        context['total_calories'] = total_calories
    except ProfileData.DoesNotExist:
        context['error'] = "Профиль данных пользователя не найден."

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
