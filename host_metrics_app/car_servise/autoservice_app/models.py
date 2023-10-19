from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)


class Order(models.Model):
    customer_nickname = models.CharField(max_length=100)
    price = models.IntegerField(default=0)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    services = models.ManyToManyField('Service', through='BasketService')

    def sum_price(self):
        total_price = sum(basket_service.service.price * basket_service.quantity for basket_service in self.basketservice_set.all())
        return total_price

    number_of_services = models.IntegerField(default=0)


class BasketService(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class OrderService(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
