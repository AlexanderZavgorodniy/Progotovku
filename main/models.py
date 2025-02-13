from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length = 100)


class Dish(models.Model):
    name = models.CharField(max_length = 100)
    recept = models.TextField()
    calories = models.PositiveIntegerField()
    protein = models.PositiveIntegerField()
    fat = models.PositiveIntegerField()
    carbohydrate = models.PositiveIntegerField()


class ProductDish(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    size = models.CharField(max_length = 200)


class ProfileData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    calories_num = models.IntegerField()