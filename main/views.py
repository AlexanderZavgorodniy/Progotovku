import datetime

from django.contrib.auth import logout
from django.shortcuts import render

from main.models import Dish

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator



def index_page(request):
    recipes = Dish.objects.all()
    for recipe in recipes:
        print("название:", recipe.name)
        print("рецепт:", recipe.recept)
        print("ингредиенты:")
        for productdish in recipe.productdish_set.all():
            print("-", productdish.product.name, productdish.grams)
        print()
    context = {
        'name': 'Сашик',
        'time': datetime.datetime.now()
    }
    return render(request, 'index.html', context)


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


def registration(request):
    context = {}
    return render(request, 'register.html', context)


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
