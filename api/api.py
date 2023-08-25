from itertools import groupby
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser
from base.models import *
from .serializer import *
from .tasks import *


@api_view(['POST'])
@parser_classes([JSONParser])
def init_order(request):
    data = request.data
    name, mobile_number = data.get('name'), data.get('mobile_number')
    customer, _ = Customer.objects.get_or_create(name=name, mobile_number=mobile_number)
    if Order.objects.filter(customer_id=customer.id, status=0).exists():
        return Response({'data':'order exists'})
    Order.objects.create(customer_id=customer.id)
    return Response({'data': 'new order created'})


@api_view(['GET'])
def get_orders(request):
    queryset = Order.objects.all()
    return Response({'data': OrderSerializer(queryset, many=True).data})


@api_view(['GET'])
def get_pizza_bases(request):
    queryset = PizzaBase.objects.all()
    return Response({'data': PizzaGenericSerializer(queryset, many=True).data})


@api_view(['GET'])
def get_cheese(request):
    queryset = Cheese.objects.all()
    return Response({'data': PizzaGenericSerializer(queryset, many=True).data})


@api_view(['GET'])
def get_toppings(request):
    queryset = Topping.objects.all()
    return Response({'data': PizzaGenericSerializer(queryset, many=True).data})


@api_view(['GET'])
def get_pizzas(request):
    data = request.query_params
    order_id = data.get('order_id')
    if order_id:
        queryset = PizzaToppingRelation.objects.select_related('pizza', 'pizza__cheese', 'pizza__pizza_base', 'topping').filter(pizza__order_id=order_id).order_by('pizza_id').annotate(toppingCount=Count('pizza_id'))
    seialized_data = PizzaSerializer(queryset, many=True).data
    result = list()
    for pizza_id, data in groupby(seialized_data, key=lambda x: x.get('pizza_id')):
        d = list(data)
        toppings = [i.get('topping') for i in d]
        result.append({
            'pizza_id': pizza_id,
            'pizza_base': d[0].get('pizza_base'),
            'cheese': d[0].get('cheese'),
            'toppings': toppings
        })
    return Response({'data': result})


@api_view(['POST'])
@parser_classes([JSONParser])
def place_order(request):
    data = request.data
    order_id = data.get('order_id')
    pizza_list = data.get('pizzas', [])
    cost = 100
    total_cost = cost * len(pizza_list)
    order = Order.objects.filter(id=order_id)
    
    if not order.first():
        raise Exception('Order ID not valid.')
    if order.first().status == 1:
       return Response({'data':'Order has already been placed.'})
   
    pizzas_topping_relations_to_create = list()
    for pizza in pizza_list:
        p = Pizza(
                pizza_base_id=pizza.get('pizza_base_id'),
                cheese_id=pizza.get('cheese_id'),
                order_id=order_id
            )
        p.save()
        if pizza.get('topging_ids', []):
            pizzas_topping_relations_to_create.extend(
                [PizzaToppingRelation(pizza_id=p.id, topping_id=t_id) 
                 for t_id in pizza.get('topging_ids')])
        
    PizzaToppingRelation.objects.bulk_create(pizzas_topping_relations_to_create)
    order.update(cost=total_cost)
    initiate_long_task.delay(order_id, 0, 1)
    return Response({'data':'Order has been placed'})