from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)


class Dish(models.Model):
    name = models.CharField(max_length=100)
    recept = models.TextField()


class ProductDish(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    grams = models.PositiveIntegerField()
