from django.urls import path
from . import api

urlpatterns = [
    # GET Requests
    path('orders', api.get_orders),
    path('bases', api.get_pizza_bases),
    path('cheeses', api.get_cheese),
    path('toppings', api.get_toppings),
    path('pizzas', api.get_pizzas),
    # POST Requests
    path('init/orders', api.init_order),
    path('place/order', api.place_order),
]
