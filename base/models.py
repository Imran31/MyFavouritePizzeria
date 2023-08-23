from typing import Iterable, Optional
from django.db import models


class PizzaBase(models.Model):
    name = models.CharField(max_length=30, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cheese(models.Model):
    name = models.CharField(max_length=30, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Topping(models.Model):
    name = models.CharField(max_length=30, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    name = models.CharField(max_length=30, blank=False)
    mobile_number =  models.CharField(max_length=10, db_index=True, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    STATUSES = [
        (0, 'Init'),
        (1, 'Placed'),
        (2, 'Accepted'),
        (3, 'Preparing'),
        (4, 'Dispatched'),
        (5, 'Delivered'),
    ]
    cost = models.IntegerField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUSES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Pizza(models.Model):
    pizza_base = models.ForeignKey(PizzaBase, on_delete=models.CASCADE)
    cheese = models.ForeignKey(Cheese, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PizzaToppingRelation(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Task(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    old_value = models.IntegerField()
    new_value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "old_value", "new_value"],
                name="unique_active_foo_bar"
            )
        ]

