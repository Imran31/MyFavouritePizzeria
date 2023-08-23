from base.models import PizzaBase, Cheese, Topping

if PizzaBase.objects.count() == 0:
    PizzaBase.objects.create(name='Thin Crust')
    PizzaBase.objects.create(name='Hand Tossed')
    PizzaBase.objects.create(name='Cheese Burst')

if Cheese.objects.count() == 0:
    Cheese.objects.create(name='Regular')
    Cheese.objects.create(name='Extra Cheesey')
    Cheese.objects.create(name='Smoked Gouda Cheese')
    Cheese.objects.create(name='Mozzarella + Blue Cheese')

if Topping.objects.count() == 0:
    Topping.objects.create(name='Mushrooms')
    Topping.objects.create(name='Onions')
    Topping.objects.create(name='Bell Peppers')
    Topping.objects.create(name='Black Olives')
    Topping.objects.create(name='Sweet Corn')
    Topping.objects.create(name='Chicken')
    Topping.objects.create(name='Jalapenos')


